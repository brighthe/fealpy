import numpy as np
import gmsh
from fealpy.mesh import TriangleMesh
from typing import Union
from camera_system import CameraSystem
from scipy.optimize import fsolve
from harmonic_map import * 
from fealpy.iopt import COA
from meshing_type import MeshingType
from partition_type import PartitionType
from dataclasses import dataclass

# 重叠区域网格
@dataclass
class OverlapGroundMesh:
    """
    @brief 重叠地面区域网格
    @param mesh: 网格
    @param cam0: 相机0
    @param cam1: 相机1
    @param uv0: 网格点在相机 0 的图像中的 uv 坐标
    @param uv1: 网格点在相机 1 的图像中的 uv 坐标
    """
    mesh : list[TriangleMesh] = None
    cam0 : int = None
    cam1 : int = None
    uv0  : np.ndarray = None
    uv1  : np.ndarray = None

@dataclass
class OverlapEllipsoidMesh:
    """
    @brief 重叠椭球区域网格
    @param mesh: 网格
    @param cam0: 相机0
    @param cam1: 相机1
    @param didx0: 相机 0 狄利克雷边界条件的节点编号
    @param didx1: 相机 1 狄利克雷边界条件的节点编号
    @param dval0: 相机 0 狄利克雷边界条件的节点值
    @param dval1: 相机 1 狄利克雷边界条件的节点值
    @param uv0: 网格点在相机 0 的图像中的 uv 坐标
    @param uv1: 网格点在相机 1 的图像中的 uv 坐标
    """
    mesh : list[TriangleMesh] = None
    cam0 : int = None
    cam1 : int = None
    didx0: np.ndarray = None
    didx1: np.ndarray = None
    dval0: np.ndarray = None
    dval1: np.ndarray = None
    uv0  : np.ndarray = None
    uv1  : np.ndarray = None

@dataclass
class NonOverlapGroundMesh:
    """
    @brief 非重叠地面区域网格
    @param mesh: 网格
    @param cam: 相机
    @param uv: 网格点在相机的图像中的 uv 坐标
    """
    mesh : list[TriangleMesh] = None
    cam  : int = None
    uv   : np.ndarray = None

@dataclass
class NonOverlapEllipsoidMesh:
    """
    @brief 非重叠椭球区域网格
    @param mesh: 网格
    @param cam: 相机
    @param didx: 狄利克雷边界条件的节点编号
    @param dval: 狄利克雷边界条件的节点值
    @param uv: 网格点在相机的图像中的 uv 坐标
    """
    mesh : list[TriangleMesh] = None
    cam  : int = None
    didx : np.ndarray = None
    dval : np.ndarray = None
    uv   : np.ndarray = None

class Screen:
    def __init__(self, camera_system, carsize, scale_ratio, center_height,
                 ptype, mtype=MeshingType.TRIANGLE):
        """
        @brief: 屏幕初始化。
                1. 从相机系统获取地面特征点
                2. 优化相机参数
                3. 分区
                4. 网格化 (计算自身的特征点)
                5. 构建相机的框架特征点 (用于调和映射的边界条件)
                6. 计算 uv
        @param camera_system: 相机系统 
        @param carsize: 车辆尺寸
        @param scale_ratio: 缩放比例
        @param center_height: 车辆中心高度
        @param ptype: 分区类型
        @param mtype: 网格化类型
        """
        self.carsize = carsize
        self.scale_ratio = scale_ratio  
        self.center_height = center_height
        self.axis_length = np.array([self.carsize[i]*self.scale_ratio[i] for i
                                     in range(3)]) # 椭圆轴长

        self.camera_system = camera_system
        self.camera_system.screen = self

        self.partition_type = ptype

        self.ground_overlapmesh = [] 
        self.ground_nonoverlapmesh = [] 
        self.eillposid_overlapmesh = []
        self.eillposid_nonoverlapmesh = []

        # 判断分区类型和网格化类型
        self.meshing()
        self.compute_uv()

    def ground_mark_board(self):
        """
        @brief 获取地面标记点
        """
        gmp = []
        camsys = self.camera_system
        for i in range(6):
            ri = (i+1)%6 # 右边相邻相机
            ps0 = camsys.cameras[ i].ground_feature_points[1]
            ps1 = camsys.cameras[ri].ground_feature_points[0]
            ps2 = 0.5*camsys.cameras[ i].to_screen(ps0)
            ps2+= 0.5*camsys.cameras[ri].to_screen(ps1)
            for j in range(len(ps0)):
                gmp.append(GroundMarkPoint(i, ri, ps0[j], ps1[j], ps2[j]))
        return gmp

    def optimize(self):
        """
        相机参数优化方法，根据特征信息优化当前相机系统中的所有相机的位置和角度。
        """
        systerm = self.camera_system
        self.i=0
        def object_function(x):
            """
            @brief The object function to be optimized.
            @param x The parameters to be optimized.
            """
            self.i+=1
            print("Optimization iteration: ", self.i)
            gmp = self.ground_mark_board()
            NGMP = len(gmp)
            x = x.reshape((6, 2, 3))
            systerm.set_parameters(x)

            ## 要对齐的点在屏幕上的坐标
            gmp_screen = np.zeros([NGMP, 2, 3], dtype=np.float_)
            for i, g in enumerate(gmp): 
                cam0 = g.cam0
                point0 = g.points0
                gmp_screen[i, 0] = systerm.cameras[cam0].to_screen(point0)
                cam1 = g.cam1
                point1 = g.points1
                gmp_screen[i, 1] = systerm.cameras[cam1].to_screen(point1)

            error = np.sum((gmp_screen[:, 0] - gmp_screen[:, 1])**2)
            print("Error: ", error)
            return error

        # 6 个相机，每个相机的位置和欧拉角共 6 * 6 = 36 个参数
        init_x = np.zeros((6, 2, 3), dtype=np.float_)
        for i in range(6):
            init_x[i, 0] = self.camera_system.cameras[i].location
            init_x[i, 1] = self.camera_system.cameras[i].eular_angle
        init_x = init_x.flatten()

        #参数设置
        N = 100
        dim = 6 * 6
        ub = init_x + 0.1
        lb = init_x - 0.1
        Max_iter = 50

        opt_alg = COA(N, dim, ub, lb, Max_iter, object_function, init_x)
        bestfitness,best_position,_ = opt_alg.cal()
        print(bestfitness)
        print(best_position)

    def get_implict_function(self):
        """
        @brief 获取表示自身的隐式函数
        """
        a, b, c = self.axis_length
        z0      = self.center_height
        def f0(p):
            x = p[..., 0]
            y = p[..., 1]
            z = p[..., 2]
            return x**2/a**2 + y**2/b**2 + z**2/c**2 - 1.0
        def f1(p):
            z = p[..., 2]
            return z + z0
        return f0, f1

    def partition(self):
        """
        将屏幕区域分区，并通过分区的分割线构造特征点与特征线，可选择 PartitionType 中提供的分区方案。
        """
        def add_rectangle(p0, p1, p2, p3):
            """
            @brief 添加矩形
            """
            # 添加线
            l1 = gmsh.model.occ.addLine(p0, p1)
            l2 = gmsh.model.occ.addLine(p1, p2)
            l3 = gmsh.model.occ.addLine(p2, p3)
            l4 = gmsh.model.occ.addLine(p3, p0)
            # 添加 loop
            curve = gmsh.model.occ.addCurveLoop([l1, l2, l3, l4])
            s = gmsh.model.occ.addPlaneSurface([curve])
            return s

        l, w, h = self.carsize
        a, b, c = self.axis_length
        z0 = -self.center_height

        parameters = self.partition_type.parameters
        # 无重叠分区
        if self.partition_type == "nonoverlap":
            theta = parameters[0]
            v = 30*np.array([[-np.cos(theta), -np.sin(theta)], 
                          [np.cos(theta), -np.sin(theta)], 
                          [np.cos(theta), np.sin(theta)], 
                          [-np.cos(theta), np.sin(theta)]])
            point = np.array([[-l/2, -w/2], [l/2, -w/2], [l/2, w/2], [-l/2, w/2]],
                             dtype=np.float64)
            ps = [3, 4, 5, 6]
            planes  = []
            for i in range(4):
                pp1 = gmsh.model.occ.addPoint(point[i, 0]+v[i, 0], point[i, 1]+v[i, 1], z0)
                pp2 = gmsh.model.occ.addPoint(point[i, 0]+v[i, 0], point[i, 1]+v[i, 1], 0.0)
                pp3 = gmsh.model.occ.addPoint(point[i, 0], point[i, 1], 0.0)
                planes.append(add_rectangle(ps[i], pp1, pp2, pp3))

            point = np.array([[0, -w/2], [0, w/2]], dtype=np.float64)
            v = 30*np.array([[0, -1], [0, 1]], dtype=np.float64)
            for i in range(2):
                pp0 = gmsh.model.occ.addPoint(point[i, 0], point[i, 1], z0)
                pp1 = gmsh.model.occ.addPoint(point[i, 0]+v[i, 0], point[i, 1]+v[i, 1], z0)
                pp2 = gmsh.model.occ.addPoint(point[i, 0]+v[i, 0], point[i, 1]+v[i, 1], 0.0)
                pp3 = gmsh.model.occ.addPoint(point[i, 0], point[i, 1], 0.0)
                planes.append(add_rectangle(pp0, pp1, pp2, pp3))

            # 将屏幕分区
            frag = gmsh.model.occ.fragment([(2, 1), (2, 3)], [(2, plane) for plane in planes])
            for i in range(len(frag[1]))[2:]:
                gmsh.model.occ.remove(frag[1][i], recursive=True)

            ground = [[[10], [0]], 
                      [[12], [1]], 
                      [[13], [2]], 
                      [[11], [3]], 
                      [[9], [4]], 
                      [[8], [5]] ]

            eillposid = [[[4], [0]], 
                         [[6], [1]], 
                         [[7], [2]], 
                         [[5], [3]], 
                         [[3], [4]], 
                         [[1, 2], [5]]]

            return ground, eillposid

        # 重叠分区1
        elif self.partition_type == "overlap1":
            pass
        # 重叠分区2
        elif self.partition_type == "overlap2":
            pass
        else:
            ValueError("Not implemented!")

    def _get_didx_dval(self, mesh, cam, surfaces, tag2nid, nidxmap):
        """
        @brief 获取狄利克雷边界条件的节点编号和值
        """
        cam = self.camera_system.cameras[cam]
        f0 = lambda x : cam.projecte_to_self(x)-cam.location

        # 获取第 i 块网格的屏幕边界特征点
        feature_edge = gmsh.model.getBoundary([(2, j) for j in surfaces])

        # 获取第 i 块网格的屏幕边界特征点的编号和值
        lists = [gmsh.model.mesh.get_nodes(1, abs(ge[1])) for ge in feature_edge]
        didx = [tag2nid[ge[0]] for ge in lists] 
        dval = [f0(ge[1].reshape(-1, 3)) for ge in lists]
        didx = nidxmap[np.concatenate(didx, dtype=np.int_)]
        dval = np.concatenate(dval, axis=0)

        didx, uniqueidx = np.unique(didx, return_index=True)
        dval = dval[uniqueidx]
        return didx, dval

    def _partmeshing(self, surfaces, node, tag2nid, cams, pmesh, overlap = False, is_eillposid = False):
        """
        @brief 生成分区网格
        @param surfaces: 分区面列表
        @param tag2nid: 节点标签到节点编号的映射
        """
        cell = [gmsh.model.mesh.get_elements(2, j)[2][0] for j in surfaces]
        cell = np.concatenate(cell).reshape(-1, 3)
        cell = tag2nid[cell]

        idx = np.unique(cell)
        nidxmap = np.zeros(node.shape[0], dtype = np.int_)
        nidxmap[idx] = np.arange(idx.shape[0])
        cell = nidxmap[cell]

        pmesh.mesh = TriangleMesh(node[idx], cell)

        if is_eillposid&overlap:
            pmesh.didx0, pmesh.dval0 = self._get_didx_dval(pmesh.mesh, cams[0], surfaces, tag2nid, nidxmap)
            pmesh.didx1, pmesh.dval1 = self._get_didx_dval(pmesh.mesh, cams[1], surfaces, tag2nid, nidxmap)
        elif is_eillposid & (not overlap):
            pmesh.didx, pmesh.dval = self._get_didx_dval(pmesh.mesh, cams[0], surfaces, tag2nid, nidxmap)

    def meshing(self, theta = np.pi/6, only_ground=False):#(self, meshing_type:MeshingType):
        """
        在屏幕上生成网格，可选择 MeshingType 中提供的网格化方案。
        @param meshing_type: 网格化方案。
        @return:
        """
        gmsh.initialize()

        gmsh.option.setNumber("Mesh.MeshSizeMax", 1)  # 最大网格尺寸
        gmsh.option.setNumber("Mesh.MeshSizeMin", 0.5)    # 最小网格尺寸

        camerasys = self.camera_system

        # 构造椭球面
        l, w, h = self.carsize
        a, b, c = self.axis_length
        z0 = -self.center_height
        phi = np.arcsin(z0 / c)

        # 构造单位球面
        r = 1.0
        ball = gmsh.model.occ.addSphere(0, 0, 0, 1, 1, phi, 0)
        gmsh.model.occ.dilate([(3, ball)],0, 0, 0, a, b, c)
        gmsh.model.occ.remove([(3, ball), (2, 2)])
        ## 车辆区域
        vehicle = gmsh.model.occ.addRectangle(-l/2, -w/2, z0, l, w)
        ## 生成屏幕
        gmsh.model.occ.cut([(2, 1), (2, 3)], [(2, vehicle)])[0]

        # 分区并生成网格
        ground, eillposid = self.partition()
        gmsh.model.occ.synchronize()
        gmsh.model.mesh.generate(2)

        ## 获取节点
        node = gmsh.model.mesh.get_nodes()[1].reshape(-1, 3)
        NN = node.shape[0]

        ## 节点编号到标签的映射
        nid2tag = gmsh.model.mesh.get_nodes()[0]
        tag2nid = np.zeros(NN*2, dtype = np.int_)
        tag2nid[nid2tag] = np.arange(NN)

        # 网格分块
        ## 地面区域网格
        for i, val in enumerate(ground):
            surfaces, cam = val
            if len(cam)==2: # 重叠区域 
                pmesh = OverlapGroundMesh()
                pmesh.cam0, pmesh.cam1 = cam
                self._partmeshing(surfaces, node, tag2nid, cam, pmesh, overlap=True)
                self.ground_overlapmesh.append(pmesh)
            else:
                pmesh = NonOverlapGroundMesh()
                pmesh.cam = cam[0]
                self._partmeshing(surfaces, node, tag2nid, cam, pmesh)
                self.ground_nonoverlapmesh.append(pmesh)

        ## 椭球区域网格
        for i, val in enumerate(eillposid):
            surfaces, cam = val
            if len(cam)==2:
                pmesh = OverlapEllipsoidMesh()
                pmesh.cam0, pmesh.cam1 = cam
                self._partmeshing(surfaces, node, tag2nid, cam, pmesh, overlap=True, is_eillposid=True)
                self.eillposid_overlapmesh.append(pmesh)
            else:
                pmesh = NonOverlapEllipsoidMesh()
                pmesh.cam = cam[0]
                self._partmeshing(surfaces, node, tag2nid, cam, pmesh, is_eillposid=True)
                self.eillposid_nonoverlapmesh.append(pmesh)
        gmsh.finalize()

    def to_view_point(self, points):
        """
        将屏幕上的点或网格映射到视点，同时传递分区、特征信息。
        @param points: 屏幕上的点。
        @return: 映射到相机系统的点。
        """
        return self.camera_system.projecte_to_view_point(points)

    def sphere_to_self(self, points, center, radius):
        """
        将一个球面上的点投影到屏幕上。
        @param points: 球面上的点 (NP, 3)。
        @param center: 球心。
        @param radius: 半径。
        @return: 投影到屏幕上的点。
        """
        if len(points.shape)==1:
            points = points[None, :]
        f0, f1 = self.get_implict_function()
        ret = np.zeros_like(points)
        def sphere_to_implict_function(p, c, r, fun):
            g = lambda t : fun(c + t*(p-c))
            t = fsolve(g, 100)
            val = c + t*(p-c)
            return val

        g0 = lambda p : sphere_to_implict_function(p, center, radius, f0)
        g1 = lambda p : sphere_to_implict_function(p, center, radius, f1)
        for i, node in enumerate(points):
            val = g1(node)
            if f0(val) > 0:
                val = g0(node)
            ret[i] = val
        return ret

    def _compute_uv_of_eillposid(self, mesh, cam, didx, dval):
        """
        @brief 计算屏幕上网格点在相机系统中的uv坐标(调和映射)。
        """
        cam = self.camera_system.cameras[cam]
        node_s = mesh.entity('node').copy()
        node   = self.to_view_point(node_s)
        mesh.node = node

        data = HarmonicMapData(mesh, didx, dval)
        node = sphere_harmonic_map(data).reshape(-1, 3)
        node += cam.location
        uv = cam.to_picture(node, normalizd=True)
        uv[:, 0] = 1-uv[:, 0]
        mesh.node = node_s
        return uv

    def _compute_uv_of_ground(self, mesh, cam):
        """
        @brief 计算屏幕上网格点在相机系统中的uv坐标(无调和映射)。
        """
        cam = self.camera_system.cameras[cam]
        node = mesh.entity('node')
        cell = mesh.entity('cell')
        uv = cam.projecte_to_self(node)
        uv = cam.to_picture(uv, normalizd=True)
        uv[:, 0] = 1-uv[:, 0]
        return uv

    def compute_uv(self):
        """
        @brief 计算网格点在相机系统中的uv坐标。
        """
        # 计算重叠椭球区域网格的uv坐标
        for mesh in self.eillposid_overlapmesh:
            mesh.uv0 = self._compute_uv_of_eillposid(mesh.mesh, mesh.cam0, mesh.didx0, mesh.dval0)
            mesh.uv1 = self._compute_uv_of_eillposid(mesh,mesh, mesh.cam1, mesh.didx1, mesh.dval1)

        # 计算非重叠椭球区域网格的uv坐标
        for mesh in self.eillposid_nonoverlapmesh:
            mesh.uv = self._compute_uv_of_eillposid(mesh.mesh, mesh.cam, mesh.didx, mesh.dval)

        # 计算重叠地面区域网格的uv坐标
        for mesh in self.ground_overlapmesh:
            mesh.uv0 = self._compute_uv_of_ground(mesh.mesh, mesh.cam0)
            mesh.uv1 = self._compute_uv_of_ground(mesh.mesh, mesh.cam1)

        # 计算非重叠地面区域网格的uv坐标
        for mesh in self.ground_nonoverlapmesh:
            mesh.uv = self._compute_uv_of_ground(mesh.mesh, mesh.cam)

    def _display_mesh(self, plotter, mesh, cam, uv):
        node = mesh.entity('node')
        cell = mesh.entity('cell')
        no = np.concatenate((node[cell].reshape(-1, 3), uv[cell].reshape(-1, 2)), axis=-1, dtype=np.float32)
        plotter.add_mesh(no, cell=None, texture_path=cam.picture.fname)

    def display(self, plotter):
        """
        显示图像。
        @param plotter: 绘图器。
        """
        cameras = self.camera_system.cameras
        # 非重叠地面区域网格
        for mesh in self.ground_nonoverlapmesh:
            self._display_mesh(plotter, mesh.mesh, cameras[mesh.cam], mesh.uv)

        # 非重叠椭球区域网格
        for mesh in self.eillposid_nonoverlapmesh:
            self._display_mesh(plotter, mesh.mesh, cameras[mesh.cam], mesh.uv)

        # 重叠地面区域网格
        for mesh in self.ground_overlapmesh:
            self._display_mesh(plotter, mesh.mesh, cameras[mesh.cam0], mesh.uv0)
            self._display_mesh(plotter, mesh.mesh, cameras[mesh.cam1], mesh.uv1)

        # 重叠椭球区域网格
        for mesh in self.eillposid_overlapmesh:
            self._display_mesh(plotter, mesh.mesh, cameras[mesh.cam0], mesh.uv0)
            self._display_mesh(plotter, mesh.mesh, cameras[mesh.cam1], mesh.uv1)


