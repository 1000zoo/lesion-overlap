import json

class Lesion:
    def __init__(self, nii, name="."):
        self.nii = nii
        self.name = name
        self.load()
        
    def load(self):
        with open("data.json", 'r', encoding="UTF-8") as f:
            self.planes_data = json.load(f)


    def overlap_detection(self):
        results = dict()
        for i in self.planes_data:
            total_overlap = 0
            planes = eval(self.planes_data[i])
            temp = {}
            for index, plane in enumerate(planes):
                overlap = 0
                for x, y, z in plane:
                    overlap += 1 if self.nii[x][y][z] != 0 else 0
                
                temp[str(index)] = overlap / len(planes)
                total_overlap += overlap

            results[i] = temp
        
        return results
    
    def overlap_part(self):
        overlap = self.overlap_detection()

if __name__ == "__main__":
    l = Lesion(None, "1")