#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path

import nibabel as nib
import numpy as np


def main():
    out = Path("examples/synthetic_case")
    images_ts = out / "imagesTs"
    labels_ts = out / "labelsTs"
    images_ts.mkdir(parents=True, exist_ok=True)
    labels_ts.mkdir(parents=True, exist_ok=True)

    shape = (64, 64, 64)
    zz, yy, xx = np.indices(shape)
    image = np.random.default_rng(2026).normal(20, 3, size=shape).astype(np.float32)
    vessel = ((yy - 32) ** 2 + (xx - 32) ** 2 < 9) & (zz > 8) & (zz < 56)
    lymphatic = ((yy - 24) ** 2 + (xx - 42) ** 2 < 4) & (zz > 15) & (zz < 50)
    image[vessel] += 120
    image[lymphatic] += 80
    mask = vessel.astype(np.uint8)

    affine = np.eye(4)
    nib.save(nib.Nifti1Image(image, affine), images_ts / "synthetic_upper_mrl_0000.nii.gz")
    nib.save(nib.Nifti1Image(mask, affine), labels_ts / "synthetic_upper_mrl.nii.gz")
    print(f"Synthetic demo written to {out}")


if __name__ == "__main__":
    main()
