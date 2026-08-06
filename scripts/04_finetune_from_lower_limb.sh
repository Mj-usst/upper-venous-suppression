#!/usr/bin/env bash
set -euo pipefail

TARGET_DATASET_ID="38"
CONFIG="3d_fullres"
FOLD="0"
TRAINER="nnUNetTrainer"
PLANS="nnUNetPlans"
PRETRAINED_CHECKPOINT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-dataset-id) TARGET_DATASET_ID="$2"; shift 2 ;;
    --config) CONFIG="$2"; shift 2 ;;
    --fold) FOLD="$2"; shift 2 ;;
    --trainer) TRAINER="$2"; shift 2 ;;
    --plans) PLANS="$2"; shift 2 ;;
    --pretrained-checkpoint) PRETRAINED_CHECKPOINT="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$PRETRAINED_CHECKPOINT" ]]; then
  PRETRAINED_CHECKPOINT="$nnUNet_results/Dataset025_leg/${TRAINER}__${PLANS}__${CONFIG}/fold_${FOLD}/checkpoint_best.pth"
fi

if [[ ! -f "$PRETRAINED_CHECKPOINT" ]]; then
  echo "Pretrained checkpoint not found: $PRETRAINED_CHECKPOINT" >&2
  exit 1
fi

echo "Fine-tuning Dataset${TARGET_DATASET_ID} from: $PRETRAINED_CHECKPOINT"
nnUNetv2_train "$TARGET_DATASET_ID" "$CONFIG" "$FOLD" -tr "$TRAINER" -p "$PLANS" -pretrained_weights "$PRETRAINED_CHECKPOINT"
