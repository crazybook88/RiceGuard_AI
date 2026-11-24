"""Dataset cleaning: format checks, corrupt-file removal, duplicate detection.
Owner: Member 1 (runs in Colab or locally; never imported by Streamlit).
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from config import settings


def list_image_files(root: Path) -> List[Path]:
    """Recursively list files whose extension is in settings.ALLOWED_EXTENSIONS."""
    # TODO (Member 1): implement with Path.rglob; compare extensions case-insensitively.
    raise NotImplementedError


def is_valid_image(path: Path) -> bool:
    """Return True if PIL can open + verify() the file and it is non-empty."""
    # TODO (Member 1): use Image.open(...).verify(); catch exceptions; reject 0-byte files.
    raise NotImplementedError


def compute_file_hash(path: Path, algo: str = "sha256") -> str:
    """Exact-duplicate fingerprint (MD5/SHA256) of file bytes."""
    # TODO (Member 1): read in chunks with hashlib.
    raise NotImplementedError


def compute_phash(path: Path):
    """Perceptual hash for near-duplicate detection (imagehash.phash)."""
    # TODO (Member 1)
    raise NotImplementedError


def find_exact_duplicates(paths: List[Path]) -> Dict[str, List[Path]]:
    """Group files by exact hash. Return only groups with more than one file."""
    # TODO (Member 1)
    raise NotImplementedError


def find_near_duplicates(paths: List[Path], threshold: int = settings.PHASH_HAMMING_THRESHOLD) -> List[List[Path]]:
    """Cluster files whose pHash Hamming distance <= threshold."""
    # TODO (Member 1): beware O(n^2); explain your approach in docs/dataset_notes.md.
    raise NotImplementedError


def build_cleaned_dataset(raw_dir: Path = settings.RAW_DIR, cleaned_dir: Path = settings.CLEANED_DIR) -> Dict[str, int]:
    """Copy valid, de-duplicated images raw -> cleaned and return a report dict
    (counts computed dynamically: total, corrupt, exact_dupes, near_dupes, kept)."""
    # TODO (Member 1): never mutate raw/. Record the report in docs/dataset_notes.md.
    raise NotImplementedError
