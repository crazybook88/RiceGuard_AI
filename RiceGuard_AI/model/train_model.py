"""Training pipeline (Colab). Owner: Member 3. Never imported by app/ or main.py."""
from __future__ import annotations

from config import settings


def make_datasets():
    """Build train/val tf.data pipelines from dataset/train and dataset/validation,
    applying preprocessing.image_preprocessing.normalize (parity rule)."""
    # TODO (Member 3): keep class order consistent with settings.CLASS_NAMES.
    raise NotImplementedError


def save_class_indices(class_names) -> None:
    """Write settings.CLASS_INDICES_PATH as {class_name: index}."""
    # TODO (Member 3)
    raise NotImplementedError


def train(model_type: str = "mobilenetv2", epochs: int = 20) -> None:
    """Fit with callbacks (EarlyStopping, ModelCheckpoint, ReduceLROnPlateau),
    plot history, export settings.MODEL_PATH (.keras) + class_indices.json."""
    # TODO (Member 3): report ONLY real numbers produced by your own runs.
    raise NotImplementedError


if __name__ == "__main__":
    train()
