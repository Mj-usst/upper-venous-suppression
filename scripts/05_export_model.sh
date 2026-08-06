#!/usr/bin/env bash
set -euo pipefail

DATASET_ID="38"
CONFIG="3d_fullres"
FOLD="0"
TRAINER="nnUNetTrainer"
PLANS="nnUNetPlans"
CHECKPOINT="checkpoint_best.pth"
OUTPUT="weights/LympClear_upper_finetune127_Dataset038_finetune127_fold0_checkpoint_best.zip"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset-id) DATASET_ID="$2"; shift 2 ;;
    --config) CONFIG="$2"; shift 2 ;;
    --fold) FOLD="$2"; shift 2 ;;
    --trainer) TRAINER="$2"; shift 2 ;;
    --plans) PLANS="$2"; shift 2 ;;
    --checkpoint) CHECKPOINT="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

mkdir -p "$(dirname "$OUTPUT")"

nnUNetv2_export_model_to_zip \
  -d "$DATASET_ID" \
  -c "$CONFIG" \
  -f "$FOLD" \
  -tr "$TRAINER" \
  -p "$PLANS" \
  -chk "$CHECKPOINT" \
  -o "$OUTPUT"
