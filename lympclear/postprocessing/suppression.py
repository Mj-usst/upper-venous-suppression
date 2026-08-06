from __future__ import annotations

import numpy as np
from tqdm import tqdm


def _local_slices(index: tuple[int, int, int], shape: tuple[int, int, int], radius: int):
    z, y, x = index
    return (
        slice(max(z - radius, 0), min(z + radius + 1, shape[0])),
        slice(max(y - radius, 0), min(y + radius + 1, shape[1])),
        slice(max(x - radius, 0), min(x + radius + 1, shape[2])),
    )


def suppress_venous_signal(
    image: np.ndarray,
    venous_mask: np.ndarray,
    radius: int = 1,
    show_progress: bool = False,
) -> np.ndarray:
    """Suppress venous signal using local nonvenous median replacement.

    With ``radius=1``, each venous voxel is replaced by the median intensity
    of nonvenous voxels within a 3 × 3 × 3 neighborhood. If no nonvenous voxel
    is available, the original intensity is retained.

    Parameters
    ----------
    image:
        Three-dimensional image volume.
    venous_mask:
        Three-dimensional binary venous mask. Nonzero values are treated as vein.
    radius:
        Neighborhood radius. ``radius=1`` corresponds to 3 × 3 × 3.
    show_progress:
        Display a progress bar.

    Returns
    -------
    np.ndarray
        Venous-suppressed image with the same shape as the input.
    """
    if image.ndim != 3:
        raise ValueError(f"Expected 3D image, got shape {image.shape}")
    if venous_mask.shape != image.shape:
        raise ValueError(f"Mask shape {venous_mask.shape} does not match image shape {image.shape}")
    if radius < 1:
        raise ValueError("radius must be >= 1")

    mask = venous_mask.astype(bool)
    out = image.astype(np.float32, copy=True)
    coords = np.argwhere(mask)
    iterator = tqdm(coords, desc="Suppressing venous voxels", unit="vox") if show_progress else coords

    for coord in iterator:
        idx = tuple(int(i) for i in coord)
        slc = _local_slices(idx, image.shape, radius)
        local_img = image[slc]
        local_mask = mask[slc]
        nonvenous_values = local_img[~local_mask]
        if nonvenous_values.size > 0:
            out[idx] = float(np.median(nonvenous_values))
    return out
