"""Class audit + leakage-safe 70/15/15 split. Owner: Member 1.

Test set must stay untouched until the final evaluation.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, List, Optional

from config import settings


def audit_class_distribution(root: Path) -> Dict[str, int]:
    """Return {class_name: image_count}, computed dynamically (no hardcoded totals)."""
    # TODO (Member 1): also flag imbalance (e.g. min/max ratio) for the report.
    raise NotImplementedError


def default_group_id(path: Path) -> str:
    """Map an image to its source-leaf group (so augmented copies stay together)."""
    # TODO (Member 1): inspect real filenames. If no leaf ID exists, fall back to
    # duplicate clusters from image_loader.find_near_duplicates and document it.
    raise NotImplementedError


def group_aware_split(
    root: Path = settings.CLEANED_DIR,
    ratios: Dict[str, float] = settings.SPLIT_RATIOS,
    group_fn: Callable[[Path], str] = default_group_id,
    seed: int = settings.RANDOM_SEED,
) -> Dict[str, List[Path]]:
    """Return {'train': [...], 'validation': [...], 'test': [...]} stratified by class,
    grouped by group_fn so no group appears in two splits."""
    # TODO (Member 1): e.g. sklearn StratifiedGroupKFold / GroupShuffleSplit.
    raise NotImplementedError


def copy_split_to_folders(split: Dict[str, List[Path]]) -> None:
    """Copy files into dataset/train|validation|test/<class>/ ."""
    # TODO (Member 1)
    raise NotImplementedError


def check_leakage(split: Dict[str, List[Path]]) -> Optional[str]:
    """Return None if clean, else a description of the overlap found
    (by exact hash, pHash and group id)."""
    # TODO (Member 1): must run (and pass) before training starts.
    raise NotImplementedError
