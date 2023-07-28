import nibabel as nib
from center import *
import json


# PATH = lambda x : f"/Users/1000zoo/Documents/crps_data/crps/rois_tracts_bin/tract_{x}.nii.gz"


def each_tract_files(s=1, e=20):
    PATH = lambda x : f"/mnt/nvme1n1/JW/crps/rois_tracts_bin/tract_{x}.nii.gz"
    for i in range(s, e):
        try:
            tract = nib.load(PATH(i)).get_fdata()
            t = Tract(tract, i)
            # t.get_center_planes()
            t.plot()
        except AssertionError as err:
            print(f"{err} => {i}")

def atlas_file(s=1, e=20):
    PATH = "/home/ni3/Desktop/prog/WMTA/WMTA/JHU/JHU-ICBM-tracts-maxprob-thr25-1mm.nii.gz"
    atlas = nib.load(PATH).get_fdata()
    print(atlas.shape)
    for i in range(s, e):
        try:
            t = Tract(atlas, i)
            t.plot()
        except:
            print("ee")
    

if __name__ == "__main__":
    atlas_file()
