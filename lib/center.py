import numpy as np
import matplotlib.pyplot as plt
import random
import math

from collections import defaultdict, deque
from random import shuffle
from copy import copy

RES = 1.3
DISMAX = 12

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
    

class Tensor:
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

        for node in self.graph:
            print(node)

        fig = plt.figure()
        ax = fig.subplots(subplot_kw={"projection": "3d"})

        ax.scatter(self.X, self.Y, self.Z, linewidth=0, alpha=0.8)
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
                


def get_COM(x, y, z):
    return sum(x) // len(x), sum(y) // len(y), sum(z) // len(z)
