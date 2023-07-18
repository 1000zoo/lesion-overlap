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
    pass