import nibabel as nib
from center import *
import json


PATH = lambda x : f"/mnt/nvme1n1/JW/crps/rois_tracts_bin/tract_{x}.nii.gz"

if __name__ == "__main__":
    for i in range(1, 21):
        tract = nib.load(PATH(i)).get_fdata()
        s, e = None, None
        with open('lib/end-points.json', encoding='UTF-8') as f:
            pp = json.loads(f.read())
            s, e = eval(pp[str(i)])

        t = Tract(tract, s, e)
        t.plot()

