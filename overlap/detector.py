import json
import nibabel
import numpy as np
import os

class Lesion:
    def __init__(self, lesion_path, planes_path):
        self.nii = nibabel.load(lesion_path).get_fdata()
        self.lesion_1mm = self.nii.shape[0] > 120
        self.pp = planes_path
        self.name = lesion_path.split("/")[-1].split(".")[0]
        self.load_atlas()


    def load_atlas(self):
        if os.path.isfile(self.pp):
            with open(self.pp, 'r', encoding="UTF-8") as f:
                self.planes_data = json.load(f)
        else:
            self.planes_data = {}
            for tract in os.listdir(self.pp):
                with open(os.path.join(self.pp, tract), 'r', encoding="UTF-8") as f:
                    temp = json.load(f)

                    for t in temp:
                        self.planes_data[t] = [plane for plane in temp[t]]

        _max = float('inf')
        for p in self.planes_data:
            _max = max(_max, (max([max([max(__t) for __t in _t]) for _t in self.planes_data[p]])))
            if _max > 120:
                self.atlas_1mm = True
                return

        self.atlas_1mm = False


    ## overlap 부분 계산
    ## results => {'tract 번호': {'평면 번호': ratio, ...}, ...}
    ## info => {'max': '최대 ratio', '가장 많이 overlap된 트랙': '트랙번호', '가장 많이 Overlap 된 평면': '평면번호'} 
    def overlap_detection(self):
        results = dict()
        info = {"max": 0}
        
        for i in self.planes_data:
            planes = eval(self.planes_data[i]) if isinstance(self.planes_data[i], str) else self.planes_data[i]
            temp = []
            ov = []
            print(f"tract no: {i}\n# of planes: {len(planes)}")
            m = 1
            for index, plane in enumerate(planes):
                overlap = 0
                ov_plane = []

                for x, y, z in plane:
                    if self.lesion_1mm ^ self.atlas_1mm:
                        x = x//2 if self.atlas_1mm else x * 2
                        y = y//2 if self.atlas_1mm else y * 2
                        z = z//2 if self.atlas_1mm else z * 2

                    overlap += 1 if self.nii[x][y][z] != 0 else 0
                    if self.nii[x][y][z] != 0:
                        ov_plane.append([x, y, z])

                overlap = len(ov_plane)

                if len(plane) == 0:
                    print(f"planes: {plane}")
                    ratio = 0
                else:
                    ratio = overlap / len(plane)
                    ratio = int(ratio * 1000) / 1000

                temp.append(ratio)
                if ratio > info["max"]:
                    info = {}
                    info["max"] = ratio
                    info["tract"] = i
                    info["plane"] = index

            results[i] = temp
        
        return results, info
    

if __name__ == "__main__":
    l = Lesion(None, "1")
