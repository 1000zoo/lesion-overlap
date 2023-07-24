import nibabel as nib
from center import *
import json


# PATH = lambda x : f"/mnt/nvme1n1/JW/crps/rois_tracts_bin/tract_{x}.nii.gz"
PATH = lambda x : f"/Users/1000zoo/Documents/crps_data/crps/rois_tracts_bin/tract_{x}.nii.gz"

if __name__ == "__main__":
    for i in range(15,16):
        tract = nib.load(PATH(i)).get_fdata()
        t = Tract(tract, i)
        t.plot()

