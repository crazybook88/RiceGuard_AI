import numpy as np
import pytest
from PIL import Image

from preprocessing.image_preprocessing import preprocess_pil_image


@pytest.mark.parametrize("mode,lo,hi", [("mobilenet_v2", -1.0, 1.0), ("rescale", 0.0, 1.0)])
def test_shape_and_range(mode, lo, hi):
    img = Image.fromarray(np.random.randint(0, 256, (50, 80, 4), dtype=np.uint8), "RGBA")
    out = preprocess_pil_image(img, mode)
    assert out.shape == (1, 224, 224, 3)
    assert out.dtype == np.float32
    assert out.min() >= lo - 1e-6 and out.max() <= hi + 1e-6

# TODO (Member 6): grayscale/palette cases and a train-vs-inference parity test.
