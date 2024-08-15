from typing import Optional

from ..backend import backend_manager as bm
from ..typing import TensorLike, Index, _S

from ..mesh import HomogeneousMesh
from ..functionspace.space import FunctionSpace as _FS
from ..utils import process_coef_func
from ..functional import bilinear_integral, linear_integral, nonlinear_integral
from .integrator import (
    CellOperatorIntegrator,
    enable_cache,
    assemblymethod,
    CoefLike
)


class ScalarMassIntegrator(CellOperatorIntegrator):
    def __init__(self, coef: Optional[CoefLike]=None, q: int=3, *,
                 index: Index=_S,
                 batched: bool=False) -> None:
        super().__init__()
        self.coef = coef
        self.q = q
        self.index = index
        self.batched = batched

    @enable_cache
    def to_global_dof(self, space: _FS) -> TensorLike:
        return space.cell_to_dof()[self.index]

    @enable_cache
    def fetch(self, space: _FS):
        q = self.q
        index = self.index
        mesh = getattr(space, 'mesh', None)

        if not isinstance(mesh, HomogeneousMesh):
            raise RuntimeError("The ScalarMassIntegrator only support spaces on"
                               f"homogeneous meshes, but {type(mesh).__name__} is"
                               "not a subclass of HomoMesh.")

        cm = mesh.entity_measure('cell', index=index)
        qf = mesh.quadrature_formula(q, 'cell')
        bcs, ws = qf.get_quadrature_points_and_weights()
        phi = space.basis(bcs, index=index)
        return bcs, ws, phi, cm, index

    def assembly(self, space: _FS) -> TensorLike:
        coef = self.coef
        mesh = getattr(space, 'mesh', None)
        bcs, ws, phi, cm, index = self.fetch(space)
        val = process_coef_func(coef, bcs=bcs, mesh=mesh, etype='cell', index=index)

        return bilinear_integral(phi, phi, ws, cm, val, batched=self.batched)
    
    @assemblymethod('nonlinear')
    def nonlinear_assembly(self, space: _FS) -> TensorLike:
        uh = self.uh
        coef = self.coef
        mesh = getattr(space, 'mesh', None)
        bcs, ws, gphi, cm, index = self.fetch(space)
        val = -uh.grad_value(bcs)# (C, Q, dof_numel)
        coef = process_coef_func(coef, bcs=bcs, mesh=mesh, etype='cell', index=index)   

        return nonlinear_integral(val, gphi, ws, cm, coef, batched=self.batched), bilinear_integral(gphi, gphi, ws, cm, coef, batched=self.batched)
