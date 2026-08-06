from pathlib import Path
import nibabel as nib
import numpy as np

out = Path(__file__).resolve().parent
imagesTs = out / "imagesTs"
labelsTs = out / "labelsTs"
imagesTs.mkdir(parents=True, exist_ok=True)
labelsTs.mkdir(parents=True, exist_ok=True)
shape = (64, 64, 64)
zz, yy, xx = np.indices(shape)
rng = np.random.default_rng(2026)
image = rng.normal(20, 3, size=shape).astype(np.float32)
vessel = ((yy - 32) ** 2 + (xx - 32) ** 2 < 9) & (zz > 8) & (zz < 56)
lymph = ((yy - 24) ** 2 + (xx - 42) ** 2 < 4) & (zz > 15) & (zz < 50)
image[vessel] += 120
image[lymph] += 80
mask = vessel.astype(np.uint8)
nib.save(nib.Nifti1Image(image, np.eye(4)), imagesTs / "synthetic_upper_mrl_0000.nii.gz")
nib.save(nib.Nifti1Image(mask, np.eye(4)), labelsTs / "synthetic_upper_mrl.nii.gz")
print(f"Synthetic demo written to {out}")
