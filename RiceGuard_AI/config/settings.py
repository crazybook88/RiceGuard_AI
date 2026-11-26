"""Central configuration. EVERY constant shared between modules lives here.

Rule: no other file may hardcode class names, image size, split ratios,
thresholds or paths. Import them from this module instead.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

# ---------------------------------------------------------------- paths
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATASET_DIR: Path = BASE_DIR / "dataset"
RAW_DIR: Path = DATASET_DIR / "raw"
CLEANED_DIR: Path = DATASET_DIR / "cleaned"
TRAIN_DIR: Path = DATASET_DIR / "train"
VAL_DIR: Path = DATASET_DIR / "validation"
TEST_DIR: Path = DATASET_DIR / "test"

SAVED_MODELS_DIR: Path = BASE_DIR / "model" / "saved_models"
MODEL_PATH: Path = SAVED_MODELS_DIR / "riceguard_model.keras"
CLASS_INDICES_PATH: Path = SAVED_MODELS_DIR / "class_indices.json"

DATA_DIR: Path = BASE_DIR / "data"          # git-ignored runtime data
HISTORY_CSV: Path = DATA_DIR / "detection_history.csv"

# ---------------------------------------------------------------- images
IMG_SIZE: Tuple[int, int] = (224, 224)
ALLOWED_EXTENSIONS: Tuple[str, ...] = (".jpg", ".jpeg", ".png")
MAX_FILE_SIZE_MB: float = 10.0

# "mobilenet_v2" -> same maths as tf.keras.applications.mobilenet_v2.preprocess_input
# "rescale"      -> pixel / 255.0   (use for the Custom CNN)
PREPROCESS_MODE: str = "rescale"

# ---------------------------------------------------------------- classes
# Baseline ONLY. After training, class_indices.json (written by train_model.py)
# becomes the single source of truth and overrides this list automatically.
DEFAULT_CLASS_NAMES: List[str] = [
    "Healthy Rice Leaf",
    "Bacterial Leaf Blight",
    "Brown Spot",
    "Rice Blast",
]


def load_class_names() -> List[str]:
    """Return class names ordered by model output index."""
    if CLASS_INDICES_PATH.exists():
        mapping: Dict[str, int] = json.loads(CLASS_INDICES_PATH.read_text())
        return [name for name, _ in sorted(mapping.items(), key=lambda kv: kv[1])]
    return list(DEFAULT_CLASS_NAMES)


CLASS_NAMES: List[str] = load_class_names()

# ---------------------------------------------------------------- data split
SPLIT_RATIOS: Dict[str, float] = {"train": 0.70, "validation": 0.15, "test": 0.15}
RANDOM_SEED: int = 42
PHASH_HAMMING_THRESHOLD: int = 5   # TODO (Member 1): justify/tune after inspecting data

# ---------------------------------------------------------------- inference
CONFIDENCE_THRESHOLD: float = 0.60
USE_MOCK_MODEL: bool = True        # flip to False once a real .keras exists
