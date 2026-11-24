"""SHARED preprocessing. Training AND inference must both call this module.

Never duplicate resize / normalisation logic anywhere else (parity rule).
Owner: Member 2.
"""
from __future__ import annotations

from typing import Tuple

import numpy as np
from PIL import Image

from config import settings


def to_rgb_resized(image: Image.Image, size: Tuple[int, int] = settings.IMG_SIZE) -> Image.Image:
    """Convert any PIL image to RGB and resize it to `size`."""
    # TODO (Member 2): decide + document the resampling filter and whether to
    # handle RGBA/palette PNGs specially (e.g. composite on a white background).
    return image.convert("RGB").resize(size, Image.BILINEAR)


def normalize(array: np.ndarray, mode: str = settings.PREPROCESS_MODE) -> np.ndarray:
    """Apply model-specific normalisation to a float32 array of 0-255 pixels."""
    # TODO (Member 2): confirm this matches the backbone used in model_builder.py.
    if mode == "mobilenet_v2":
        return array / 127.5 - 1.0          # -> [-1, 1]
    if mode == "rescale":
        return array / 255.0                # -> [0, 1]
    raise ValueError(f"Unknown PREPROCESS_MODE: {mode!r}")


def preprocess_pil_image(image: Image.Image, mode: str = settings.PREPROCESS_MODE) -> np.ndarray:
    """Full pipeline for ONE image. Returns float32 array of shape (1, H, W, 3)."""
    rgb = to_rgb_resized(image)
    arr = np.asarray(rgb, dtype=np.float32)
    arr = normalize(arr, mode)
    return np.expand_dims(arr, axis=0)
