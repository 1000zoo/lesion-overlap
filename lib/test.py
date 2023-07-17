import nibabel as nib
import matplotlib.pyplot as plt
import json
import networkx as nx
from queue import PriorityQueue as pq

class Test:
    def __init__(self, x) -> None:
        self.x = x

    def __str__(self):
        return self.x

    def __sub__(self, y):
        assert isinstance(y, Test)
        return self.x - y.x


def sqm(x1, x2):
    return (x1 - x2) ** 2

# def get_centerline(self, interval=2):
#         short = self.short_path()
#         centers = []

#         vectors = get_vectors(short)

#         for i, xyz in enumerate(short):
#             if i == len(short) - 1:
#                 break
#             x, y, z = xyz
#             vector = vectors[i]
#             centers.append(self.min_area_plane_center(x, y, z, vector))

#         centers.append(self.end)
            
#         return [center[0] for center in centers], [center[1] for center in centers], [center[2] for center in centers]



if __name__ == "__main__":
    # from collections import defaultdict

    # dd = defaultdict()
    # dd[(1,2,3)] = "as"
    # dd[(2,3,4)] = "bb"

    # # print((1,2,3) in dd)
    # s = -0.5
    # e = 0.5
    # n = 5
    # lin = [k for k in range(s, e, (e - s) / n)]
    # print(lin)

    centerlines = ([50, 48, 48, 49, 48, 49, 50, 51, 52, 54, 55, 55, 56, 56, 56, 56], [48, 51, 52, 57, 55, 59, 62, 63, 65, 68, 75, 77, 79, 81, 83, 85], [41, 40, 40, 38, 38, 38, 38, 39, 40, 40, 39, 40, 39, 37, 37, 37])
    tx, ty, tz = centerlines
    centerlines = [(i, j, k) for i, j, k in zip(tx, ty, tz)]
