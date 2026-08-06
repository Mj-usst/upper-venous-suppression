#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

import imageio.v2 as imageio
import numpy as np

from lympclear.io.nifti import load_nifti
from lympclear.visualization.mip import save_mip_png, save_cine_gif
from lympclear.postprocessing.highlighting import normalize_window


def parse_args():
    p = argparse.ArgumentParser(description="Create MIP PNG and optional cine GIF from a 3D/4D NIfTI image.")
    p.add_argument("--image", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--axis", type=int, default=0)
    p.add_argument("--make-gif", action="store_true")
    p.add_argument("--fps", type=float, default=2.0)
    return p.parse_args()


def main():
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data, _ = load_nifti(args.image)

    if data.ndim == 3:
        save_mip_png(data, out_dir / "mip.png", axis=args.axis)
    elif data.ndim == 4:
        frames = []
        for t in range(data.shape[-1]):
            vol = data[..., t]
            mip = np.max(vol, axis=args.axis)
            arr = normalize_window(mip)
            png = (arr * 255).astype(np.uint8)
            imageio.imwrite(out_dir / f"mip_phase{t:02d}.png", png)
            frames.append(mip)
        if args.make_gif:
            save_cine_gif(frames, out_dir / "mip_cine.gif", fps=args.fps)
    else:
        raise ValueError(f"Expected 3D or 4D image, got shape {data.shape}")

    print(f"Saved MIP/cine outputs to: {out_dir}")


if __name__ == "__main__":
    main()
