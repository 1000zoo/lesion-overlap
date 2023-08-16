# written by Jiwoo Chun, at 2023-07-29
# modified with numpy by Cheol E. Han at 2023-08-02 (supported by chat-GPT)
import numpy as np
import matplotlib.pyplot as plt
import json

RES = 2.5
INTERVAL = 5

class Tract:
    def __init__(self, nii, num):
        self.nii = nii
        self.num = num
        self.tensor = np.argwhere(self.nii == self.num)
        self.centerline = None
        self.center_plane = []

    def load_marked_point(self, filename):
        with open(filename, encoding='UTF-8') as f:
            mp = json.loads(f.read())
            self.marked_points = np.array(mp, dtype=int)

    def plot(self, title="."):
        fig = plt.figure()
        ax = fig.subplots(subplot_kw={"projection": "3d"})
        ax.scatter(self.tensor[:, 0], self.tensor[:, 1], self.tensor[:, 2], linewidth=0, alpha=0.1, label="tracts")
        # ax.scatter(self.marked_points[:,0], self.marked_points[:,1], self.marked_points[:,2], c='r', label="marked points")
        ax.plot(self.centerline[:,0], self.centerline[:,1], self.centerline[:,2], color='red', marker='x', markersize=5, label="center lines")
        for i, plane in enumerate(self.center_planes):
            ax.scatter(plane[:,0],plane[:,1],plane[:,2], linewidths=1, label=str(i))
        ax.legend()
        ax.set_xlim([min(self.tensor[:, 0]), max(self.tensor[:, 0])])
        ax.set_ylim([min(self.tensor[:, 1]), max(self.tensor[:, 1])])
        ax.set_zlim([min(self.tensor[:, 2]), max(self.tensor[:, 2])])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        plt.title(title)
        plt.show()
        plt.close()

    def get_cross_section_area(self, point, vector):
        # tensor에서 관심 있는 영역만 선택
        mask_range = np.all((self.tensor >= (point-INTERVAL) ) & (self.tensor <= (point+INTERVAL)), axis=1)
        selected_tensor = self.tensor[mask_range]
        # Main Loop
        equation = lambda _x, _y, _z: abs(np.dot(vector, [_x, _y, _z]) + np.dot(vector, -np.array(point)))
        mask_area = np.apply_along_axis(lambda xyz: equation(*xyz), 1, selected_tensor) < RES
        area = np.sum(mask_area)
        return area, selected_tensor[mask_area]

    def min_area_plane_center(self, point0, vector):
        lin = np.linspace(-0.5, 0.5, 5)
        uv = [norm(vector) + np.array((i, j, k)) for i in lin for j in lin for k in lin]
        uv = np.unique(uv, axis=0)  # 중복 제거

        areas = [self.get_cross_section_area(point0, vec)[0] for vec in uv]
        min_index = np.argmin(areas)
        _, min_plane = self.get_cross_section_area(point0, uv[min_index])
        return np.mean(min_plane, axis=0)

    def get_center_planes(self):
        if self.centerline is None:
            self.get_centerline()
        self.center_planes = []
        # smoothed tangent vector
        for prev_point, curr_point, next_point in zip(self.centerline[:-2], self.centerline[1:-1], self.centerline[2:]):
            vector1 = curr_point - prev_point
            vector2 = next_point - curr_point
            vector = (vector1 + vector2) / 2
            _, plane = self.get_cross_section_area(curr_point, vector)
            self.center_planes.append(plane)

    def save_planes(self, filename):
        planes_as_list = [plane.tolist() for plane in self.center_planes]
        with open(filename, 'r', encoding="UTF-8") as f:
            temp = json.load(f)
        with open(filename, 'w', encoding="UTF-8") as f:
            temp[str(self.num)] = planes_as_list
            json.dump(temp, f, ensure_ascii=False, indent='\t')

    def get_centerline(self, interval=1):
        marked = np.array(self.marked_points)
        centers = [marked[0]]
        for curr, xyz in zip(marked[:-1], marked[1:]):
            vector = xyz - curr
            centers.append(self.min_area_plane_center(xyz, vector))
        self.centerline = np.array(centers)

def norm(v: np.ndarray):
    roots = np.linalg.norm(v)
    if roots == 0:
        return None
    return v / roots
