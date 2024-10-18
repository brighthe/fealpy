from fealpy.backend import backend_manager as bm
from fealpy.opt.optimizer_base import opt_alg_options
import matplotlib.pyplot as plt

def ciyt0():
    citys = bm.array([
    [101.7400, 6.5600],
    [112.5300, 37.8700],
    [121.4700, 31.2300],
    [119.3000, 26.0800],
    [106.7100, 26.5700],
    [103.7300, 36.0300],
    [111.6500, 40.8200],
    [120.1900, 30.2600],
    [121.3000, 25.0300],
    [106.5500, 29.5600],
    [106.2700, 38.4700],
    [116.4000, 39.9000],
    [118.7800, 32.0400],
    [114.1700, 22.3200],
    [104.0600, 30.6700],
    [108.9500, 34.2700],
    [117.2000, 39.0800],
    [117.2700, 31.8600],
    [113.5400, 22.1900],
    [102.7300, 25.0400],
    [113.6500, 34.7600],
    [123.3800, 41.8000],
    [114.3100, 30.5200],
    [113.2300, 23.1600],
    [91.1100, 29.9700],
    [117.0000, 36.6500],
    [125.3500, 43.8800],
    [113.0000, 28.2100],
    [110.3500, 20.0200],
    [87.6800, 43.7700],
    [114.4800, 38.0300],
    [126.6300, 45.7500],
    [115.8900, 28.6800],
    [108.3300, 22.8400]
    ])
    return citys

def city_ulysses22():
    citys = bm.array([
        [38.24, 20.42],
        [39.57, 26.15],
        [40.56, 25.32],
        [36.26, 23.12],
        [33.48, 10.54],
        [37.56, 12.19],
        [38.42, 13.11],
        [37.52, 20.44],
        [41.23, 9.10],
        [41.17, 13.05],
        [36.08, -5.21],
        [38.47, 15.13],
        [38.15, 15.35],
        [37.51, 15.17],
        [35.49, 14.32],
        [39.36, 19.56],
        [38.09, 24.36],
        [36.09, 23.00],
        [40.44, 13.57],
        [40.33, 14.15],
        [40.37, 14.23],
        [37.57, 22.56]
    ])
    return citys

def city_ulysses16():
    citys = bm.array([
        [38.24, 20.42],
        [39.57, 26.15],
        [40.56, 25.32],
        [36.26, 23.12],
        [33.48, 10.54],
        [37.56, 12.19],
        [38.42, 13.11],
        [37.52, 20.44],
        [41.23, 9.10],
        [41.17, 13.05],
        [36.08, -5.21],
        [38.47, 15.13],
        [38.15, 15.35],
        [37.51, 15.17],
        [35.49, 14.32],
        [39.36, 19.56]
    ])
    return citys

def city_att48():
    citys = bm.array([
        [6734, 1453],
        [2233, 10],
        [5530, 1424],
        [401, 841],
        [3082, 1644],
        [7608, 4458],
        [7573, 3716],
        [7265, 1268],
        [6898, 1885],
        [1112, 2049],
        [5468, 2606],
        [5989, 2873],
        [4706, 2674],
        [4612, 2035],
        [6347, 2683],
        [6107, 669],
        [7611, 5184],
        [7462, 3590],
        [7732, 4723],
        [5900, 3561],
        [4483, 3369],
        [6101, 1110],
        [5199, 2182],
        [1633, 2809],
        [4307, 2322],
        [675, 1006],
        [7555, 4819],
        [7541, 3981],
        [3177, 756],
        [7352, 4506],
        [7545, 2801],
        [3245, 3305],
        [6426, 3173],
        [4608, 1198],
        [23, 2216],
        [7248, 3779],
        [7762, 4595],
        [7392, 2244],
        [3484, 2829],
        [6271, 2135],
        [4985, 140],
        [1916, 1569],
        [7280, 4899],
        [7509, 3239],
        [10, 2676],
        [6807, 2993],
        [5185, 3258],
        [3023, 1942]
    ])
    return citys

def city_chn31():
    citys = bm.array([
        [1304, 2312],
        [3639, 1315],
        [4177, 2244],
        [3712, 1399],
        [3488, 1535],
        [3326, 1556],
        [3238, 1229],
        [4196, 1004],
        [4312, 790],
        [4386, 570],
        [3007, 1970],
        [2562, 1756],
        [2788, 1491],
        [2381, 1676],
        [1332, 695],
        [3715, 1678],
        [3918, 2179],
        [4061, 2370],
        [3780, 2212],
        [3676, 2578],
        [4029, 2838],
        [4263, 2931],
        [3429, 1908],
        [3507, 2367],
        [3394, 2643],
        [3439, 3201],
        [2935, 3240],
        [3140, 3550],
        [2545, 2357],
        [2778, 2826],
        [2370, 2975]
    ])
    return citys

def city_eil51():
    citys = bm.array([
        [37, 52],
        [49, 49],
        [52, 64],
        [20, 26],
        [40, 30],
        [21, 47],
        [17, 63],
        [31, 62],
        [52, 33],
        [51, 21],
        [42, 41],
        [31, 32],
        [5, 25],
        [12, 42],
        [36, 16],
        [52, 41],
        [27, 23],
        [17, 33],
        [13, 13],
        [57, 58],
        [62, 42],
        [42, 57],
        [16, 57],
        [8, 52],
        [7, 38],
        [27, 68],
        [30, 48],
        [43, 67],
        [58, 48],
        [58, 27],
        [37, 69],
        [38, 46],
        [46, 10],
        [61, 33],
        [62, 63],
        [63, 69],
        [32, 22],
        [45, 35],
        [59, 15],
        [5, 6],
        [10, 17],
        [21, 10],
        [5, 64],
        [30, 15],
        [39, 10],
        [32, 39],
        [25, 32],
        [25, 55],
        [48, 28],
        [56, 37],
        [30, 40]
    ])
    return citys

def city_oliver30():
    citys = bm.array([
        [5, 2, 99],
        [10, 4, 50],
        [6, 7, 64],
        [11, 13, 40],
        [12, 18, 40],
        [9, 18, 54],
        [8, 22, 60],
        [13, 24, 42],
        [14, 25, 38],
        [7, 25, 62],
        [3, 37, 84],
        [16, 41, 26],
        [4, 41, 94],
        [15, 44, 35],
        [17, 45, 21],
        [2, 54, 62],
        [1, 54, 67],
        [18, 58, 35],
        [30, 58, 69],
        [19, 62, 32],
        [24, 64, 60],
        [25, 68, 58],
        [23, 71, 44],
        [29, 71, 71],
        [28, 74, 78],
        [20, 82, 7],
        [22, 83, 46],
        [26, 83, 69],
        [27, 87, 76],
        [21, 91, 38]
    ])
    return citys

def city_rand50():
    citys = bm.array([
        [475, 110],
        [29, 929],
        [755, 897],
        [698, 979],
        [871, 317],
        [535, 184],
        [548, 73],
        [594, 380],
        [233, 845],
        [881, 654],
        [200, 540],
        [9, 800],
        [526, 456],
        [765, 30],
        [992, 449],
        [659, 193],
        [938, 370],
        [233, 966],
        [692, 112],
        [680, 873],
        [589, 968],
        [553, 444],
        [106, 941],
        [959, 366],
        [273, 614],
        [568, 383],
        [661, 431],
        [824, 144],
        [191, 587],
        [464, 457],
        [959, 722],
        [823, 486],
        [259, 513],
        [977, 467],
        [794, 895],
        [243, 863],
        [802, 294],
        [811, 650],
        [954, 534],
        [300, 486],
        [665, 865],
        [648, 205],
        [645, 848],
        [29, 496],
        [98, 25],
        [344, 676],
        [735, 371],
        [924, 450],
        [313, 472],
        [407, 339]
    ])
    return citys

def city_3():
    citys = bm.array([
        [475, 110, 112],
        [29, 929, 873],
        [755, 897, 968],
        [698, 979, 444],
        [871, 317, 941],
        [535, 184, 366],
        [548, 73, 614],
        [594, 380, 383],
        [233, 845, 431],
        [881, 654, 144],
        [200, 540, 587],
        [9, 800, 457],
        [526, 456, 722],
        [765, 30, 486],
        [992, 449, 513],
        [659, 193, 467],
        [938, 370, 895],
        [233, 966, 863]
    ])
    return citys

TSP_data = [
    {
        "citys": ciyt0,
        "dim": 34,
    },
    {
        "citys":city_ulysses22,
        "dim":22,
        "opt":74,
    },
    {
        "citys": city_ulysses16,
        "dim": 16,
        "opt":72,
    },
    {
        "citys": city_att48,
        "dim": 48,
        "opt":33522,
    },
    {
        "citys": city_chn31,
        "dim": 31,
        "opt":15377,
    },
    {
        "citys": city_eil51,
        "dim": 51,
        "opt":426,
    },
    {
        "citys": city_oliver30,
        "dim": 30,
        "opt":420,
    },
    {
        "citys": city_rand50,
        "dim": 50,
        "opt":5553,
    },
    {
        "citys": city_3,
        "dim": 18,
    },
]


def soler_tsp_with_ant(algorithm, fobj, lb, ub, NP, dim, D):
    x0 = lb + bm.random.rand(NP, dim) * (ub - lb)
    option = opt_alg_options(x0, fobj, (lb, ub), NP, MaxIters = 10000)
    optimizer = algorithm(option, D)
    gbest, gbest_f = optimizer.run()
    return gbest, gbest_f

def soler_tsp_with_algorithm(algorithm, fobj, lb, ub, NP, dim, D):
    x0 = lb + bm.random.rand(NP, dim) * (ub - lb)
    option = opt_alg_options(x0, fobj, (lb, ub), NP, MaxIters = 10000)
    optimizer = algorithm(option, D)
    gbest, gbest_f = optimizer.run()
    return gbest, gbest_f

def gbest2route(gbest, citys):
    route = bm.argsort(gbest)
    route = bm.concatenate((route, route[0: 1]))
    route_citys = citys[route]
    return route, route_citys

def printroute(route_citys, citys, alg_name):
    dim = citys.shape[1]
    if dim == 2:
        for i in range(route_citys.shape[0]):
            plt.figure()
            plt.title(f"{alg_name[i]} optimal path")
            plt.scatter(citys[:, 0], citys[:, 1])
            plt.plot(route_citys[i, :, 0], route_citys[i, :, 1])
    elif dim == 3:
        for i in range(route_citys.shape[0]):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.set_title(f"{alg_name[i]} optimal path")
            ax.scatter(citys[:, 0], citys[:, 1], citys[:, 2]) 
            ax.plot(route_citys[i, :, 0], route_citys[i, :, 1], route_citys[i, :, 2])
    plt.show()

def calD(citys):
    n = citys.shape[0]
    D = bm.zeros((n, n)) 
    diff = citys[:, None, :] - citys[None, :, :]
    D = bm.sqrt(bm.sum(diff ** 2, axis = -1))
    D[bm.arange(n), bm.arange(n)] = 2.2204e-16
    return D

class TravellingSalesmanProblem:
    def __init__(self, citys) -> None:
        self.citys = citys
        self.D = bm.zeros((citys.shape[0], citys.shape[0]))
    
    def fitness(self, x):
        index = bm.argsort(x, axis=-1)
        distance = self.D[index[:, -1], index[:, 0]]
        for i in range(x.shape[1] - 1):
            dis = self.D[index[:, i], index[:, i + 1]]
            distance = distance + dis
        return distance

    def calD(self):
        n = self.citys.shape[0] 
        diff = self.citys[:, None, :] - self.citys[None, :, :]
        self.D = bm.sqrt(bm.sum(diff ** 2, axis = -1))
        self.D[bm.arange(n), bm.arange(n)] = 2.2204e-16
        
        





if __name__ == "__main":
    pass