from __future__ import annotations

from pathlib import Path
from typing import Tuple

import nibabel as nib
import numpy as np


def load_nifti(path: str | Path) -> Tuple[np.ndarray, nib.Nifti1Image]:
    """Load a NIfTI image and return data as float32 plus the original image object."""
    img = nib.load(str(path))
    data = np.asarray(img.get_fdata(dtype=np.float32))
    return data, img


def load_mask(path: str | Path, threshold: float = 0.5) -> Tuple[np.ndarray, nib.Nifti1Image]:
    """Load a binary mask from NIfTI."""
    data, img = load_nifti(path)
    return (data > threshold), img


def save_nifti(data: np.ndarray, reference_img: nib.Nifti1Image, output_path: str | Path) -> None:
    """Save data as NIfTI while preserving affine and header from a reference image."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    header = reference_img.header.copy()
    out_img = nib.Nifti1Image(data, reference_img.affine, header=header)
    nib.save(out_img, str(output_path))
