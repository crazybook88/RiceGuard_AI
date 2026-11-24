"""Model architectures. Owner: Member 3. Colab/GPU only; never imported by app/."""
from __future__ import annotations

from typing import Tuple

from config import settings


def build_mobilenetv2(num_classes: int, input_shape: Tuple[int, int, int] = (*settings.IMG_SIZE, 3),
                      freeze_base: bool = True):
    """Transfer-learning model: MobileNetV2 (include_top=False) + classification head.
    Must pair with settings.PREPROCESS_MODE == 'mobilenet_v2'."""
    # TODO (Member 3): import tensorflow INSIDE the function; build + return a compiled model.
    raise NotImplementedError


def build_custom_cnn(num_classes: int, input_shape: Tuple[int, int, int] = (*settings.IMG_SIZE, 3)):
    """Small baseline CNN. Must pair with settings.PREPROCESS_MODE == 'rescale'."""
    # TODO (Member 3)
    raise NotImplementedError
