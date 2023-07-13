import numpy as np
import matplotlib.pyplot as plt
import random
import math

from collections import defaultdict, deque
from random import shuffle
from copy import copy
from queue import PriorityQueue

RES = 1.53
DISMAX = 10

class Node:
    def __init__(self, points: tuple):
        x, y, z = points
        self.x = x
        self.y = y
        self.z = z
        self.points = points
        self.neighbors = []
        

    def __str__(self) -> str:
        return f"Node: ({self.x}, {self.y}, {self.z})"
    
    def get_points(self):
        return self.points
    
    def add_neighbor(self, node):
        self.neighbors.append(node)

    def set_neighbor(self, neighbors):
        self.neighbors = neighbors

    def is_surface(self):
        return len(self.neighbors) < 23
    

class Tract:
    def __init__(self, nii, start=None, end=None):
        self.nii = nii
        self.start = start
        self.end = end
        self.tensor = []
        self.graph = []
        self.X, self.Y, self.Z = [], [], []
        self.pnmap = defaultdict(Node)
        self.set_graph()
        self.set_connection()
        self.com = get_COM(self.X, self.Y, self.Z)
        self.plimit = self.get_index_limit()


    def get_index_limit(self):
        return max(max(self.X) - min(self.X), max(self.Y) - min(self.Y), max(self.Z) - min(self.Z)) + 1
    

    def plot(self, title=".", p=True):
        _max = self.plimit / 2
        xcom, ycom, zcom = self.com

        fig = plt.figure()
        ax = fig.subplots(subplot_kw={"projection": "3d"})

        ax.scatter(self.X, self.Y, self.Z, linewidth=0, alpha=0.4)
        if self.start and self.end:
            sx, sy, sz = self.get_centerline()
            ax.scatter(sx, sy, sz, linewidth=1, alpha=0.8, c='r')
            short = self.short_path()
            sx, sy, sz = [c[0] for c in short], [c[1] for c in short], [c[2] for c in short]
            ax.scatter(sx, sy, sz, linewidth=1, alpha=0.8, c='y')

        ax.set_xlim([xcom - _max, xcom + _max])
        ax.set_ylim([ycom - _max, ycom + _max])
        ax.set_zlim([zcom - _max, zcom + _max])

        plt.title(title)
        plt.show()
        plt.close()


    def set_graph(self):
        for i, x in enumerate(self.nii):
            for j, y in enumerate(x):
                for k, z in enumerate(y):
                    if z == 1.0:
                        self.tensor.append((i, j, k))
                        temp = Node((i, j, k))
                        self.graph.append(temp)
                        self.pnmap[(i, j, k)] = temp
        
        
        for tensor in self.tensor:
            _x, _y, _z = tensor
            self.X.append(_x)
            self.Y.append(_y)
            self.Z.append(_z)


    def set_connection(self):
        unit = [-1, 0, 1]
        uv = [(i, j, k) for i in unit for j in unit for k in unit if (not i == j == k == 0)]

        for x, y, z in self.tensor:
            node = self.pnmap[(x, y, z)]
            neighbors = []

            for i, j, k in uv:
                dx, dy, dz = x + i, y + j, z + k

                if (dx, dy, dz) in self.tensor:
                    neighbor = self.pnmap[(dx, dy, dz)]
                    neighbors.append(neighbor)

                node.set_neighbor(neighbors)


    def min_area_plane_center(self, x0, y0, z0, vector):
        lin = [x for x in np.linspace(-0.5, 0.5, 5)]
        uv = [add_vector(norm(vector), (i, j, k)) for i in lin for j in lin for k in lin]

        uv = list(set(uv))
        xin, yin, zin = [], [], []
        min_area = float('inf')
        min_nv = None

        for i, j, k in uv:
            area = 0
            d = -1 * (i * x0 + j * y0 + k * z0)
            equation = lambda _x, _y, _z: abs(i * _x + j * _y + k * _z + d)
            distance = lambda _x, _y, _z: math.sqrt(((_x - x0) ** 2) + (_y - y0) ** 2 + (_z - z0) ** 2)
            tx, ty, tz = [], [], []

            for x, y, z in self.tensor:
                res = equation(x, y, z)
                if res < RES and distance(x, y, z) < DISMAX:
                    area += 1
                    tx.append(x)
                    ty.append(y)
                    tz.append(z)

            if area < min_area:
                min_area = area
                min_nv = (i, j, k)
                xin = tx
                yin = ty
                zin = tz

        return get_COM(xin, yin, zin)

    def get_centerline(self, interval=1):
        short = self.short_path()
        curr = short.pop(0)
        centers = [curr]

        for i, xyz in enumerate(short):
            x, y, z = xyz
            vector = sub_vector(curr, xyz)
            centers.append(self.min_area_plane_center(x, y, z, vector))
            curr = xyz

        centers.append(self.end)
        # rc = []
        # for i in range(0, len(centers), interval):
        #     rc.append(centers[i])
            
        # return [center[0] for center in rc], [center[1] for center in rc], [center[2] for center in rc]
        return [center[0] for center in centers], [center[1] for center in centers], [center[2] for center in centers]



    def short_path(self, interval=5):
        start, end = self.pnmap[self.start], self.pnmap[self.end]

        q = deque()
        visited = set()
        history = defaultdict(list)
        last_node = None
        q.append(start)

        while q:
            curr = q.popleft()
            curr_history = history[curr]
            curr_history.append(curr)
            if curr == end:
                break
            for node in curr.neighbors:
                if not node in visited:
                    q.append(node)
                    visited.add(node)
                    history[node] = curr_history + [node]
                    last_node = node

        if end not in visited:
            history[end] = history[last_node] + [end]

        short_cut = []

        for i in range(0, len(history[end]), interval):
            short_cut.append(history[end][i])


        return [(node.x, node.y, node.z) for node in short_cut]

                

def dist(n1: Node, n2: Node):
    x = msq(n1.x, n2.x)
    y = msq(n1.y, n2.y)
    z = msq(n1.z, n2.z)
    return math.sqrt(x + y + z)

def msq(x1, x2):
    return (x1 - x2) ** 2

def get_vectors(points):
    assert len(points) > 1
    vectors = []

    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        vectors.append(sub_vector(p2, p1))

    return vectors


def sub_vector(t1, t2):
    assert len(t1) == 3 and len(t2) == 3
    t2 = scalar_mul(t2, -1)
    return add_vector(t1, t2)

def add_vector(t1, t2):
    assert len(t1) == 3 and len(t2) == 3 ## (x,y,z) 형식만
    temp = []

    for o1, o2 in zip(t1, t2):
        temp.append(o1+o2)

    return tuple(temp)

def scalar_mul(v: tuple, k):
    assert len(v) == 3
    return k * v[0], k * v[1], k * v[2]


def norm(v: tuple):
    i, j, k = v
    roots = math.sqrt(i ** 2 + j ** 2 + k ** 2)
    if roots == 0:
        return None
    return i / roots, j / roots, k / roots


def get_COM(x, y, z):
    return sum(x) // len(x), sum(y) // len(y), sum(z) // len(z)
