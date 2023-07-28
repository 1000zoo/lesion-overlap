import json

class Lesion:
    def __init__(self, nii, name="."):
        self.nii = nii
        self.name = name
        self.load()
        

    def load(self):
        with open("data.json", 'r', encoding="UTF-8") as f:
            self.planes_data = json.load(f)

    ## overlap 부분 계산
    ## results => {'tract 번호': {'평면 번호': ratio, ...}, ...}
    ## info => {'max': '최대 ratio', '가장 많이 overlap된 트랙': '트랙번호', '가장 많이 Overlap 된 평면': '평면번호'} 
    def overlap_detection(self):
        results = dict()
        info = {"max": 0}
        
        for i in self.planes_data:
            total_overlap = 0
            planes = eval(self.planes_data[i])
            temp = {}
            for index, plane in enumerate(planes):
                overlap = 0
                for x, y, z in plane:
                    overlap += 1 if self.nii[x][y][z] != 0 else 0
                
                if overlap == 0 or len(plane) == 0:
                    continue
                
                ratio = overlap / len(plane)
                ratio = int(ratio * 1000) / 1000
                temp[str(index)] = ratio
                if ratio > info["max"]:
                    info = {}
                    info["max"] = ratio
                    info["tract"] = i
                    info["plane"] = index
                    
                total_overlap += overlap

            results[i] = temp
        
        return results, info
    

if __name__ == "__main__":
    l = Lesion(None, "1")
