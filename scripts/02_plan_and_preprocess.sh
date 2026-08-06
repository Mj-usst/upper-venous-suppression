#!/usr/bin/env bash
set -euo pipefail

DATASET_ID=""
VERIFY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset-id) DATASET_ID="$2"; shift 2 ;;
    --verify) VERIFY="--verify_dataset_integrity"; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$DATASET_ID" ]]; then
  echo "Usage: bash scripts/02_plan_and_preprocess.sh --dataset-id 38 [--verify]" >&2
  exit 1
fi

nnUNetv2_plan_and_preprocess -d "$DATASET_ID" $VERIFY
