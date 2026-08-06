from __future__ import annotations

import os
from pathlib import Path


def get_nnunet_path(env_name: str) -> Path:
    value = os.environ.get(env_name)
    if not value:
        raise EnvironmentError(f"Environment variable {env_name} is not set")
    return Path(value)


def default_checkpoint_path(
    dataset_name: str,
    fold: int = 0,
    checkpoint: str = "checkpoint_best.pth",
    trainer: str = "nnUNetTrainer",
    plans: str = "nnUNetPlans",
    configuration: str = "3d_fullres",
) -> Path:
    results = get_nnunet_path("nnUNet_results")
    return results / dataset_name / f"{trainer}__{plans}__{configuration}" / f"fold_{fold}" / checkpoint
