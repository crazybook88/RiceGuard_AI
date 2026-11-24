import numpy as np
from PIL import Image

from config import settings
from model.predict import predict_image


def test_mock_schema():
    img = Image.fromarray(np.zeros((32, 32, 3), dtype=np.uint8))
    r = predict_image(img, use_mock=True)
    assert set(r) == {"predicted_class", "confidence", "probabilities", "is_low_confidence", "is_mock"}
    assert r["is_mock"] is True
    assert r["predicted_class"] in settings.CLASS_NAMES
    assert abs(sum(r["probabilities"].values()) - 1.0) < 1e-6

# TODO (Member 6): low-confidence flag logic and mock determinism.
