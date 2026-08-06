from __future__ import annotations

from pathlib import Path
from typing import Iterable

import imageio.v2 as imageio
import numpy as np

from lympclear.postprocessing.highlighting import normalize_window


def maximum_intensity_projection(volume: np.ndarray, axis: int = 0) -> np.ndarray:
    if axis not in (0, 1, 2):
        raise ValueError("axis must be 0, 1, or 2")
    return np.max(volume, axis=axis)


def save_grayscale_png(array2d: np.ndarray, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    arr = normalize_window(array2d)
    imageio.imwrite(str(output_path), (arr * 255).astype(np.uint8))


def save_mip_png(volume: np.ndarray, output_path: str | Path, axis: int = 0) -> None:
    mip = maximum_intensity_projection(volume, axis=axis)
    save_grayscale_png(mip, output_path)


def save_cine_gif(frames: Iterable[np.ndarray], output_path: str | Path, fps: float = 2.0) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rendered = []
    for frame in frames:
        arr = normalize_window(frame)
        rendered.append((arr * 255).astype(np.uint8))
    imageio.mimsave(str(output_path), rendered, duration=1.0 / fps)
