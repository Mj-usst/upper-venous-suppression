from __future__ import annotations

import numpy as np


def dice_score(pred: np.ndarray, target: np.ndarray, eps: float = 1e-8) -> float:
    """Compute binary Dice score."""
    p = pred.astype(bool)
    t = target.astype(bool)
    intersection = np.logical_and(p, t).sum(dtype=np.float64)
    denom = p.sum(dtype=np.float64) + t.sum(dtype=np.float64)
    if denom == 0:
        return 1.0
    return float((2.0 * intersection + eps) / (denom + eps))


def bootstrap_mean_ci(values, n_boot: int = 2000, ci: float = 95.0, seed: int = 2026):
    """Bootstrap mean and percentile confidence interval."""
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("values must not be empty")
    rng = np.random.default_rng(seed)
    samples = rng.choice(arr, size=(n_boot, arr.size), replace=True).mean(axis=1)
    alpha = (100.0 - ci) / 2.0
    lo, hi = np.percentile(samples, [alpha, 100.0 - alpha])
    return float(arr.mean()), float(lo), float(hi)
