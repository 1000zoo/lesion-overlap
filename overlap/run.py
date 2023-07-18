import nibabel as nib
from detector import *
import json

PATH = "/mnt/nvme1n1/JW/crps/lesion/ROI_C14_FLAIR.nii"

if __name__ == "__main__":
    nii = nib.load(PATH).get_fdata()
    l = Lesion(nii)
    r, i = l.overlap_detection()


    print(f"r => \n{r}")
    print(f"\ni => \n{i}")