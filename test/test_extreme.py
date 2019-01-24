import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from fealpy.mesh import TriangleMesh
from fealpy.functionspace.lagrange_fem_space import LagrangeFiniteElementSpace
from fealpy.mesh import Tritree

class Estimator:
    def __init__(self, rho, mesh, theta, beta):
        self.mesh = mesh
        self.rho = rho
        self.theta = theta
        self.beta = beta
        self.area = mesh.entity_measure('cell')
        self.compute_eta()
        self.maxeta = np.max(self.eta)

    def compute_eta(self):
        mesh = self.mesh
        cell = mesh.entity('cell')
        Dlambda = mesh.grad_lambda()
        grad = np.einsum('ij, ijm->im', self.rho[cell], Dlambda)
        self.eta = np.sqrt(np.sum(grad**2, axis=1)*self.area)
        return self.eta

    def update(self, rho, mesh, smooth=True):
        self.rho = rho
        self.mesh = mesh
        self.area = mesh.entity_measure('cell')
        if smooth is True:
            self.smooth_rho()
        self.compute_eta()

    def is_extreme_node(self):

        mesh = self.mesh
        NN = mesh.number_of_nodes()
        edge = mesh.entity('edge')

        isSmall = self.rho[edge[:, 0]] < self.rho[edge[:, 1]]
        minv = np.zeros(NN, dtype=np.int)
        maxv = np.zeros(NN, dtype=np.int)
        np.add.at(minv, edge[isSmall, 0], -1)
        np.add.at(minv, edge[~isSmall, 1], -1)
        np.add.at(maxv, edge[isSmall, 1], 1)
        np.add.at(maxv, edge[~isSmall, 0], 1)
        node2node = mesh.ds.node_to_node()
        V = np.sum(node2node, axis=1)

        isExtremeNode = (np.abs(minv) == V) | (np.abs(maxv) == V)
        return isExtremeNode

    def smooth_rho(self):
        '''
        smooth the rho
        '''
        mesh = self.mesh
        cell = mesh.entity('cell')
        isExtremeNode = self.is_extreme_node()
        node2cell = mesh.ds.node_to_cell()
        inva = 1/self.area
        s = node2cell@inva
        for i in range(2):
            crho = (self.rho[cell[:, 0]] + self.rho[cell[:, 1]] + self.rho[cell[:, 2]])/3.0
            rho = np.asarray(node2cell@(crho*inva))/s
            self.rho[~isExtremeNode] = rho[~isExtremeNode]

    def is_uniform(self):
        stde = np.std(self.eta)/self.maxeta
        print('The current relative std of eta is ', stde)
        if stde < 0.025:
            return True
        else:
            return False

def peak(p):
    x = p[..., 0]
    y = p[..., 1]
    val = 3*(1-x)**2*np.exp(-(x**2)-(y+1)**2) - 10*(x/5 - pow(x, 3) - pow(y, 5))*np.exp(-x**2-y**2) - 1/3*np.exp(-(x+1)**2-y**2)
    return val

node = np.array([
    (0, 0), 
    (1, 0), 
    (1, 1),
    (0, 1)], dtype=np.float)
cell = np.array([
    (1, 2, 0),
    (3, 0, 2)], dtype=np.int)

mesh = TriangleMesh(node, cell)
mesh.uniform_refine(4)
node = mesh.entity('node')
cell = mesh.entity('cell')
tmesh = Tritree(node, cell)

femspace = LagrangeFiniteElementSpace(mesh, p=1) 
uI = femspace.interpolation(peak)
estimator = Estimator(uI[:], mesh, 0.3, 0.5)
isExtremeNode = estimator.is_extreme_node()
print(isExtremeNode.sum())






















x, y = np.meshgrid(node[:, 0], node[:, 1])
#u = peak(node)
#fig = plt.figure()
#ax = Axes3D(fig)
#ax.plot_surface(x, y, u, rstride=1, cstride=1, cmap=cm.viridis)
#
#plt.show()
