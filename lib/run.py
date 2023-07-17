import nibabel as nib
from center import *
import json


PATH = lambda x : f"/mnt/nvme1n1/JW/crps/rois_tracts_bin/tract_{x}.nii.gz"

if __name__ == "__main__":
    for i in range(1, 2):
        tract = nib.load(PATH(i)).get_fdata()
        t = Tract(tract, i)
        t.plot()

