"""SHARED preprocessing. Training AND inference must both call this module.

Never duplicate resize / normalisation logic anywhere else (parity rule).
Owner: Member 2.
"""
from __future__ import annotations

from typing import Tuple

import numpy as np
from PIL import Image, ImageOps

from config import settings

# Pillow >= 9.1 uses Image.Resampling; older versions use Image.LANCZOS.
try:
    _RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:  # pragma: no cover
    _RESAMPLE = Image.LANCZOS


def _flatten_transparency(image: Image.Image) -> Image.Image:
    """Composite any image with transparency onto a white background."""
    has_alpha = image.mode in ("RGBA", "LA", "PA", "RGBa", "La") or (
        image.mode == "P" and "transparency" in image.info
    )
    if not has_alpha:
        return image
    rgba = image.convert("RGBA")
    background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    return Image.alpha_composite(background, rgba)


def to_rgb_resized(image: Image.Image, size: Tuple[int, int] = settings.IMG_SIZE) -> Image.Image:
    """Convert any PIL image to RGB and resize it to `size`."""
    image = ImageOps.exif_transpose(image)       # fix phone-photo rotation
    image = _flatten_transparency(image)         # RGBA / palette PNG handling
    return image.convert("RGB").resize(size, _RESAMPLE)


def normalize(array: np.ndarray, mode: str = settings.PREPROCESS_MODE) -> np.ndarray:
    """Apply model-specific normalisation to a float32 array of 0-255 pixels."""
    array = array.astype(np.float32, copy=False)
    if mode == "mobilenet_v2":
        return (array / 127.5 - 1.0).astype(np.float32)   # -> [-1, 1]
    if mode == "rescale":
        return (array / 255.0).astype(np.float32)         # -> [0, 1]
    raise ValueError(f"Unknown PREPROCESS_MODE: {mode!r}")


def preprocess_pil_image(image: Image.Image, mode: str = settings.PREPROCESS_MODE) -> np.ndarray:
    """Full pipeline for ONE image. Returns float32 array of shape (1, H, W, 3)."""
    rgb = to_rgb_resized(image)
    arr = np.asarray(rgb, dtype=np.float32)
    arr = normalize(arr, mode)
    return np.expand_dims(arr, axis=0)
