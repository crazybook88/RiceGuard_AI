"""Inference engine used by the Streamlit app. Owner: Member 4.

Public contract (do NOT change without telling the whole team):

    predict_image(image, use_mock=None) -> {
        "predicted_class": str,
        "confidence": float,                  # 0-1
        "probabilities": {class_name: float}, # sums to ~1
        "is_low_confidence": bool,
        "is_mock": bool,
    }
"""
from __future__ import annotations

import hashlib
from functools import lru_cache
from typing import Dict, Optional

import numpy as np
from PIL import Image

from config import settings
from preprocessing.image_preprocessing import preprocess_pil_image  # noqa: F401 (used by real_predict)


def _build_result(probs: np.ndarray, is_mock: bool) -> Dict:
    names = settings.CLASS_NAMES
    idx = int(np.argmax(probs))
    return {
        "predicted_class": names[idx],
        "confidence": float(probs[idx]),
        "probabilities": {n: float(p) for n, p in zip(names, probs)},
        "is_low_confidence": bool(probs[idx] < settings.CONFIDENCE_THRESHOLD),
        "is_mock": is_mock,
    }


def mock_predict(image: Image.Image) -> Dict:
    """Deterministic FAKE prediction so UI work can start before training.
    Always flagged is_mock=True so the UI can show a 'demo only' banner."""
    seed = int(hashlib.md5(image.tobytes()).hexdigest()[:8], 16)
    probs = np.random.default_rng(seed).dirichlet(np.ones(len(settings.CLASS_NAMES)))
    return _build_result(probs, is_mock=True)


@lru_cache(maxsize=1)
def load_model(model_path: str = str(settings.MODEL_PATH)):
    """Load the .keras model once (cached)."""
    # TODO (Member 4): import tensorflow here (lazy); raise FileNotFoundError with a
    # friendly message if the file is missing.
    raise NotImplementedError


def real_predict(image: Image.Image) -> Dict:
    """Run the real model."""
    # TODO (Member 4): x = preprocess_pil_image(image); probs = load_model().predict(x)[0];
    # return _build_result(probs, is_mock=False)
    raise NotImplementedError


def predict_image(image: Image.Image, use_mock: Optional[bool] = None) -> Dict:
    """Single entry point for the UI."""
    use_mock = settings.USE_MOCK_MODEL if use_mock is None else use_mock
    return mock_predict(image) if use_mock else real_predict(image)
