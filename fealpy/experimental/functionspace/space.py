
from typing import Union, Callable, Optional, Any

from ..typing import TensorLike, Index, Number, _S, Size
from .function import Function
from .utils import zero_dofs


class FunctionSpace():
    r"""The base class of function spaces"""
    ftype: Any
    itype: Any

    # basis
    def basis(self, p: TensorLike, index: Index=_S, **kwargs) -> TensorLike: raise NotImplementedError
    def grad_basis(self, p: TensorLike, index: Index=_S, **kwargs) -> TensorLike: raise NotImplementedError
    def hess_basis(self, p: TensorLike, index: Index=_S, **kwargs) -> TensorLike: raise NotImplementedError

    # values
    def value(self, uh: TensorLike, p: TensorLike, index: Index=_S) -> TensorLike: raise NotImplementedError
    def grad_value(self, uh: TensorLike, p: TensorLike, index: Index=_S) -> TensorLike: raise NotImplementedError

    # counters
    def number_of_global_dofs(self) -> int: raise NotImplementedError
    def number_of_local_dofs(self, doftype='cell') -> int: raise NotImplementedError

    # relationships
    def cell_to_dof(self) -> TensorLike: raise NotImplementedError
    def face_to_dof(self) -> TensorLike: raise NotImplementedError

    # interpolation
    def interpolate(self, source: Union[Callable[..., TensorLike], TensorLike, Number],
                    uh: TensorLike, dim: Optional[int]=None, index: Index=_S) -> TensorLike:
        raise NotImplementedError

    # function
    def array(self, dim: Union[Size, int, None]=None) -> TensorLike:
        """Initialize a Tensor filled with zeros as values of DoFs.

        Parameters:
            dim (Tuple[int, ...] | int | None, optional): Shape of DoFs. Defaults to None.

        Returns:
            Tensor: Values of DoFs shaped (GDOF, *dim).
        """
        GDOF = self.number_of_global_dofs()
        return zero_dofs(GDOF, dim, dtype=self.ftype)

    def function(self, data: Optional[TensorLike]=None, /, dim: Union[Size, int, None]=None):
        """Initialize a Function in the space.

        Parameters:
            data (TensorLike): Values of DoFs shaped (GDOF, *dim). Defaults to None.\n
            dim (Tuple[int, ...] | int | None, optional): Shape of DoFs.
                None or 0 for scalar dofs, int for vector dofs, and int tuple for tensor dofs.
                Defaults to None.

        Returns:
            Function: A Function object.
        """
        if data is None:
            data = self.array(dim=dim)
        return Function(self, data)
