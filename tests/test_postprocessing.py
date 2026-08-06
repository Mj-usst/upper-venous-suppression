import numpy as np

from lympclear.postprocessing.suppression import suppress_venous_signal
from lympclear.metrics.dice import dice_score


def test_suppression_local_nonvenous_median_center_voxel():
    image = np.ones((3, 3, 3), dtype=np.float32) * 10
    image[1, 1, 1] = 100
    mask = np.zeros_like(image, dtype=bool)
    mask[1, 1, 1] = True
    out = suppress_venous_signal(image, mask, radius=1)
    assert out[1, 1, 1] == 10


def test_dice_score():
    a = np.array([1, 1, 0, 0])
    b = np.array([1, 0, 1, 0])
    assert abs(dice_score(a, b) - 0.5) < 1e-6
