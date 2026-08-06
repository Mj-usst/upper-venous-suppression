#!/usr/bin/env bash
set -euo pipefail

MODEL_ZIP=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model-zip) MODEL_ZIP="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$MODEL_ZIP" ]]; then
  echo "Usage: bash scripts/06_install_model.sh --model-zip /path/to/model.zip" >&2
  exit 1
fi

if [[ ! -f "$MODEL_ZIP" ]]; then
  echo "Model archive not found: $MODEL_ZIP" >&2
  exit 1
fi

nnUNetv2_install_pretrained_model_from_zip "$MODEL_ZIP"
