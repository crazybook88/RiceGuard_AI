"""
Test set must stay untouched until the final evaluation.
"""
from __future__ import annotations
from pathlib import Path
from typing import Callable, Dict, List, Optional
from config import settings
from preprocessing.image_loader import list_image_files, find_exact_duplicates, find_near_duplicates
from sklearn.model_selection import StratifiedGroupKFold

import shutil

def audit_class_distribution(root: Path) -> Dict[str, int]:
    """Count the images in each class folder."""
    counts = {}

    # Check each class folder
    for class_folder in root.iterdir():

        if class_folder.is_dir():
            # Count all image files in this folder
            image_count = sum(
                1 for file in class_folder.rglob("*")
                if file.is_file()
                and file.suffix.lower() in settings.ALLOWED_EXTENSIONS
            )

            counts[class_folder.name] = image_count

    return counts


def default_group_id(path: Path) -> str:
    """Return a unique ID for each image."""
    return str(path)


def group_aware_split(
    root: Path = settings.CLEANED_DIR,
    ratios: Dict[str, float] = settings.SPLIT_RATIOS,
    group_fn: Callable[[Path], str] = default_group_id,
    seed: int = settings.RANDOM_SEED,
) -> Dict[str, List[Path]]:
    """Split images into train, validation and test sets."""

    # Get all image files
    files = list_image_files(root)

    # Get the class name of each image
    labels = [file.parent.name for file in files]

    # Find near-duplicate groups only once
    near_duplicates = find_near_duplicates(files)

    # Assign the same group ID to similar images
    group_map = {}

    for index, group in enumerate(near_duplicates):
        for file in group:
            group_map[file] = f"group_{index}"

    # Get the group ID for each image
    groups = [
        group_map.get(file, group_fn(file))
        for file in files
    ]

    # Divide the dataset into 20 folds
    splitter = StratifiedGroupKFold(
        n_splits=20,
        shuffle=True,
        random_state=seed
    )

    # Calculate how many folds belong to each split
    train_end = round(ratios["train"] * 20)
    val_end = train_end + round(ratios["validation"] * 20)

    split = {
        "train": [],
        "validation": [],
        "test": []
    }

    # Assign each fold to its split
    for fold_index, (_, test_indices) in enumerate(
        splitter.split(files, labels, groups)
    ):
        if fold_index < train_end:
            split_name = "train"
        elif fold_index < val_end:
            split_name = "validation"
        else:
            split_name = "test"

        for index in test_indices:
            split[split_name].append(files[index])

    return split



def copy_split_to_folders(split: Dict[str, List[Path]]) -> None:
    """Copy images into train, validation and test folders."""

    # Copy images into their respective folders
    for split_name, files in split.items():
        for file in files:

            # Create the class folder
            class_folder = settings.DATASET_DIR / split_name / file.parent.name
            class_folder.mkdir(parents=True, exist_ok=True)

            # Copy the image
            destination = class_folder / file.name
            shutil.copy2(file, destination)


def check_leakage(split: Dict[str, List[Path]]) -> Optional[str]:
    """Check whether duplicate images appear in different splits."""

    # Combine all images from the three splits
    all_files = (
        split["train"]
        + split["validation"]
        + split["test"]
    )

    # Record which split each image belongs to
    file_splits = {}

    for split_name, files in split.items():
        for file in files:
            file_splits[file] = split_name

    # Check exact duplicates
    exact_duplicates = find_exact_duplicates(all_files)

    for group in exact_duplicates:
        group_splits = set(file_splits[file] for file in group)

        if len(group_splits) > 1:
            return "Exact duplicate leakage detected."

    # Check near-duplicate images
    near_duplicates = find_near_duplicates(all_files)

    for group in near_duplicates:
        group_splits = set(file_splits[file] for file in group)

        if len(group_splits) > 1:
            return "Near-duplicate leakage detected."

    # No leakage found
    return None
