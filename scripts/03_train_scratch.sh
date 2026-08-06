#!/usr/bin/env bash
set -euo pipefail

DATASET_ID="29"
CONFIG="3d_fullres"
FOLD="0"
TRAINER="nnUNetTrainer"
PLANS="nnUNetPlans"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset-id) DATASET_ID="$2"; shift 2 ;;
    --config) CONFIG="$2"; shift 2 ;;
    --fold) FOLD="$2"; shift 2 ;;
    --trainer) TRAINER="$2"; shift 2 ;;
    --plans) PLANS="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

nnUNetv2_train "$DATASET_ID" "$CONFIG" "$FOLD" -tr "$TRAINER" -p "$PLANS"
