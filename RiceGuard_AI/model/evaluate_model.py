"""Test-set evaluation. Owner: Member 4. Run once, at the very end."""
from __future__ import annotations

from config import settings


def evaluate(model_path=settings.MODEL_PATH, test_dir=settings.TEST_DIR) -> dict:
    """Return accuracy, per-class precision/recall/F1, confusion matrix (sklearn)."""
    # TODO (Member 4): load model, iterate test set WITHOUT shuffling, compute metrics.
    raise NotImplementedError


def plot_confusion_matrix(cm, class_names, out_path) -> None:
    """Save a confusion-matrix PNG with matplotlib."""
    # TODO (Member 4)
    raise NotImplementedError
