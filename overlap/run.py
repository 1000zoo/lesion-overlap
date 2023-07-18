import nibabel as nib
from detector import *
import json

PATH = "/mnt/nvme1n1/JW/crps/lesion/ROI_C22_CT.nii"

if __name__ == "__main__":
    nii = nib.load(PATH).get_fdata()
    l = Lesion(nii)
    print(l.overlap_detection())
