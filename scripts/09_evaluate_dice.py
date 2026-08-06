#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from lympclear.io.nifti import load_mask
from lympclear.metrics.dice import bootstrap_mean_ci, dice_score


def parse_args():
    p = argparse.ArgumentParser(description="Evaluate binary venous segmentation Dice.")
    p.add_argument("--pairs-csv", required=True, help="CSV with case_id,pred_path,label_path,center columns")
    p.add_argument("--output-csv", required=True)
    p.add_argument("--summary-csv", default=None)
    p.add_argument("--n-boot", type=int, default=2000)
    p.add_argument("--seed", type=int, default=2026)
    return p.parse_args()


def main():
    args = parse_args()
    df = pd.read_csv(args.pairs_csv)
    rows = []
    for _, row in df.iterrows():
        pred, _ = load_mask(row["pred_path"])
        target, _ = load_mask(row["label_path"])
        rows.append({
            "case_id": row.get("case_id", ""),
            "center": row.get("center", ""),
            "dice": dice_score(pred, target),
        })
    out = pd.DataFrame(rows)
    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)

    if args.summary_csv:
        summaries = []
        group_cols = ["center"] if "center" in out.columns else []
        if group_cols:
            for center, sub in out.groupby("center"):
                mean, lo, hi = bootstrap_mean_ci(sub["dice"].values, n_boot=args.n_boot, seed=args.seed)
                summaries.append({"center": center, "n": len(sub), "mean_dice": mean, "ci_low": lo, "ci_high": hi})
        mean, lo, hi = bootstrap_mean_ci(out["dice"].values, n_boot=args.n_boot, seed=args.seed)
        summaries.append({"center": "ALL", "n": len(out), "mean_dice": mean, "ci_low": lo, "ci_high": hi})
        pd.DataFrame(summaries).to_csv(args.summary_csv, index=False)

    print(out.describe(include="all"))


if __name__ == "__main__":
    main()
