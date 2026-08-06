#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

import pandas as pd


def parse_args():
    p = argparse.ArgumentParser(description="Prepare an nnU-Net v2 dataset from a CSV manifest.")
    p.add_argument("--manifest", required=True, help="CSV with case_id,image_path,label_path,split columns")
    p.add_argument("--dataset-id", required=True, type=int, help="nnU-Net dataset ID, e.g. 38")
    p.add_argument("--dataset-name", required=True, help="Dataset name suffix, e.g. finetune127")
    p.add_argument("--output-root", default=None, help="Defaults to $nnUNet_raw")
    p.add_argument("--channel-name", default="postcontrast_T1w_MRL")
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    out_root = Path(args.output_root or os.environ.get("nnUNet_raw", ""))
    if not out_root:
        raise RuntimeError("Set --output-root or $nnUNet_raw")
    dataset_dir = out_root / f"Dataset{args.dataset_id:03d}_{args.dataset_name}"
    if dataset_dir.exists() and args.overwrite:
        shutil.rmtree(dataset_dir)
    dataset_dir.mkdir(parents=True, exist_ok=True)
    imagesTr = dataset_dir / "imagesTr"
    labelsTr = dataset_dir / "labelsTr"
    imagesTs = dataset_dir / "imagesTs"
    imagesTr.mkdir(exist_ok=True)
    labelsTr.mkdir(exist_ok=True)
    imagesTs.mkdir(exist_ok=True)

    df = pd.read_csv(args.manifest)
    required = {"case_id", "image_path", "split"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    num_training = 0
    for _, row in df.iterrows():
        case_id = str(row["case_id"])
        split = str(row["split"]).lower()
        image_path = Path(row["image_path"])
        if not image_path.exists():
            raise FileNotFoundError(image_path)

        if split in {"train", "tr", "training", "val", "validation"}:
            dst_img = imagesTr / f"{case_id}_0000.nii.gz"
            shutil.copy2(image_path, dst_img)
            label_path = row.get("label_path", "")
            if isinstance(label_path, str) and label_path.strip():
                label_path = Path(label_path)
                if not label_path.exists():
                    raise FileNotFoundError(label_path)
                shutil.copy2(label_path, labelsTr / f"{case_id}.nii.gz")
            else:
                raise ValueError(f"Training case {case_id} has no label_path")
            num_training += 1
        elif split in {"test", "ts", "testing", "infer", "inference"}:
            shutil.copy2(image_path, imagesTs / f"{case_id}_0000.nii.gz")
        else:
            raise ValueError(f"Unsupported split: {split}")

    dataset_json = {
        "channel_names": {"0": args.channel_name},
        "labels": {"background": 0, "vein": 1},
        "numTraining": num_training,
        "file_ending": ".nii.gz",
    }
    (dataset_dir / "dataset.json").write_text(json.dumps(dataset_json, indent=2), encoding="utf-8")
    print(f"Prepared {dataset_dir}")
    print(f"numTraining = {num_training}")


if __name__ == "__main__":
    main()
