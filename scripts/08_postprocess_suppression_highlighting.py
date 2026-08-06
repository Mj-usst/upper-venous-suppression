#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

import imageio.v2 as imageio

from lympclear.io.nifti import load_mask, load_nifti, save_nifti
from lympclear.postprocessing.highlighting import make_highlight_mip, make_highlighted_volume
from lympclear.postprocessing.suppression import suppress_venous_signal


def parse_args():
    p = argparse.ArgumentParser(description="Generate venous-suppressed and venous-highlighted outputs.")
    p.add_argument("--image", required=True, help="Input NIfTI image")
    p.add_argument("--mask", required=True, help="Predicted venous mask NIfTI")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--mode", choices=["suppression", "highlight", "both"], default="both")
    p.add_argument("--radius", type=int, default=1, help="1 means 3x3x3 local nonvenous median")
    p.add_argument("--mip-axis", type=int, default=0)
    p.add_argument("--show-progress", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    image, img_obj = load_nifti(args.image)
    mask, _ = load_mask(args.mask)

    if args.mode in {"suppression", "both"}:
        suppressed = suppress_venous_signal(image, mask, radius=args.radius, show_progress=args.show_progress)
        save_nifti(suppressed, img_obj, out_dir / "suppressed.nii.gz")

    if args.mode in {"highlight", "both"}:
        highlighted_volume = make_highlighted_volume(image, mask)
        save_nifti(highlighted_volume, img_obj, out_dir / "highlighted_intensity_boost.nii.gz")
        highlight_mip = make_highlight_mip(image, mask, axis=args.mip_axis)
        imageio.imwrite(out_dir / "highlighted_mip.png", highlight_mip)

    print(f"Saved outputs to: {out_dir}")


if __name__ == "__main__":
    main()
