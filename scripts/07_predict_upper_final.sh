#!/usr/bin/env bash
set -euo pipefail

INPUT=""
OUTPUT="outputs/pred_venous_mask"
DATASET_ID="38"
CONFIG="3d_fullres"
FOLD="0"
TRAINER="nnUNetTrainer"
PLANS="nnUNetPlans"
CHECKPOINT="checkpoint_best.pth"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input) INPUT="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --dataset-id) DATASET_ID="$2"; shift 2 ;;
    --config) CONFIG="$2"; shift 2 ;;
    --fold) FOLD="$2"; shift 2 ;;
    --trainer) TRAINER="$2"; shift 2 ;;
    --plans) PLANS="$2"; shift 2 ;;
    --checkpoint) CHECKPOINT="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$INPUT" ]]; then
  echo "Usage: bash scripts/07_predict_upper_final.sh --input imagesTs --output outputs/pred" >&2
  exit 1
fi

mkdir -p "$OUTPUT"

nnUNetv2_predict \
  -i "$INPUT" \
  -o "$OUTPUT" \
  -d "$DATASET_ID" \
  -c "$CONFIG" \
  -f "$FOLD" \
  -tr "$TRAINER" \
  -p "$PLANS" \
  -chk "$CHECKPOINT"
