from __future__ import annotations

import numpy as np


def normalize_window(image: np.ndarray, lower_percentile: float = 1.0, upper_percentile: float = 99.0) -> np.ndarray:
    """Percentile-window image normalization to [0, 1]."""
    lo, hi = np.percentile(image[np.isfinite(image)], [lower_percentile, upper_percentile])
    if hi <= lo:
        hi = lo + 1.0
    out = (image.astype(np.float32) - lo) / (hi - lo)
    return np.clip(out, 0.0, 1.0)


def make_highlight_mip(
    image: np.ndarray,
    venous_mask: np.ndarray,
    axis: int = 0,
    alpha: float = 0.45,
    lower_percentile: float = 1.0,
    upper_percentile: float = 99.0,
) -> np.ndarray:
    """Create an RGB MIP with venous structures overlaid.

    The grayscale MIP is preserved and mask-positive voxels are displayed as a
    conspicuous red overlay. The returned image is uint8 RGB.
    """
    if image.shape != venous_mask.shape:
        raise ValueError("image and venous_mask must have the same shape")
    if axis not in (0, 1, 2):
        raise ValueError("axis must be 0, 1, or 2")

    img_norm = normalize_window(image, lower_percentile, upper_percentile)
    gray_mip = np.max(img_norm, axis=axis)
    mask_mip = np.max(venous_mask.astype(np.uint8), axis=axis).astype(bool)

    rgb = np.stack([gray_mip, gray_mip, gray_mip], axis=-1)
    overlay = np.zeros_like(rgb)
    overlay[..., 0] = 1.0

    rgb[mask_mip] = (1.0 - alpha) * rgb[mask_mip] + alpha * overlay[mask_mip]
    return (np.clip(rgb, 0.0, 1.0) * 255).astype(np.uint8)


def make_highlighted_volume(image: np.ndarray, venous_mask: np.ndarray, boost: float = 1.25) -> np.ndarray:
    """Create an intensity-preserving highlighted volume for simple NIfTI export.

    This is not a colored DICOM export. It preserves the original grayscale image and
    boosts mask-positive voxels for quick quality-control visualization.
    """
    out = image.astype(np.float32, copy=True)
    if np.any(venous_mask):
        high = np.percentile(image[np.isfinite(image)], 99.5)
        out[venous_mask.astype(bool)] = np.maximum(out[venous_mask.astype(bool)] * boost, high)
    return out
