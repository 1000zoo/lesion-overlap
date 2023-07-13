import nibabel as nib
import matplotlib.pyplot as plt
import json


if __name__ == "__main__":
    with open('lib/end-points.json', encoding='UTF-8') as f:
        pp = json.loads(f.read())
        print(eval(pp['1'])[0][1])