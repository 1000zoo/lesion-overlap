import nibabel as nib
from center import *


PATH = lambda x : f"/mnt/nvme1n1/JW/crps/rois_tracts_bin/tract_{x}.nii.gz"

if __name__ == "__main__":
    # for i in range(1, 21):
    tract = nib.load(PATH(17)).get_fdata()
    
    t = Tensor(tract)
    t.plot()

