#Dataset cleaning and duplicate detection.
from __future__ import annotations

import hashlib
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import imagehash
from PIL import Image

from config import settings


def list_image_files(root: Path) -> List[Path]:
    """Find all image files in the given folder."""

    image_files = []

    # Search through all folders and files.
    for path in root.rglob("*"):

        # Only include files with allowed image formats.
        if path.is_file() and path.suffix.lower() in settings.ALLOWED_EXTENSIONS:
            image_files.append(path)

    return sorted(image_files)


def is_valid_image(path: Path) -> bool:
    """Check whether an image can be opened and read."""

    try:
        # Check if the file is empty.
        if path.stat().st_size == 0:
            return False

        # Check whether the image file is valid.
        with Image.open(path) as img:
            img.verify()

        return True

    except Exception:
        return False


def compute_file_hash(path: Path, algo: str = "sha256") -> str:
    """Calculate the hash value of a file."""

    hasher = hashlib.new(algo)

    # Read the file in small parts.
    with open(path, "rb") as file:
        while True:
            chunk = file.read(8192)

            if not chunk:
                break

            hasher.update(chunk)

    return hasher.hexdigest()


def compute_phash(path: Path):
    """Calculate the perceptual hash of an image."""

    # Open the image and calculate its pHash.
    with Image.open(path) as img:
        return imagehash.phash(img)


def find_exact_duplicates(paths: List[Path]) -> Dict[str, List[Path]]:
    """Find images with exactly the same file content."""

    hash_groups = defaultdict(list)

    # Group images that have the same hash value.
    for path in paths:
        file_hash = compute_file_hash(path)
        hash_groups[file_hash].append(path)

    # Return groups that contain more than one image.
    duplicates = {
        file_hash: files
        for file_hash, files in hash_groups.items()
        if len(files) > 1
    }

    return duplicates


def find_near_duplicates(paths: List[Path], threshold: int = settings.PHASH_HAMMING_THRESHOLD) -> List[List[Path]]:
    """Find images that look similar to each other."""

    # Calculate the pHash for every image.
    hashes = {
        path: compute_phash(path)
        for path in paths
    }

    # Start with each image in its own group.
    groups = {path: {path} for path in paths}

    # Compare each pair of images.
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):

            image1 = paths[i]
            image2 = paths[j]

            # Calculate the difference between two pHashes.
            distance = hashes[image1] - hashes[image2]

            if distance <= threshold:

                group1 = groups[image1]
                group2 = groups[image2]

                # Join the groups if the images are similar.
                if group1 is not group2:
                    merged_group = group1 | group2

                    for path in merged_group:
                        groups[path] = merged_group

    # Keep only groups that contain multiple images.
    unique_groups = {}

    for group in groups.values():
        if len(group) > 1:
            key = tuple(sorted(str(path) for path in group))
            unique_groups[key] = sorted(group)

    return list(unique_groups.values())


def build_cleaned_dataset(raw_dir: Path = settings.RAW_DIR, cleaned_dir: Path = settings.CLEANED_DIR) -> Dict[str, int]:
    """Copy valid images without exact duplicates into the cleaned folder."""

    # Get all image files
    files = list_image_files(raw_dir)

    # Keep only valid images
    valid_files = [f for f in files if is_valid_image(f)]

    # Find exact duplicates
    exact_duplicates = find_exact_duplicates(valid_files)

    # Find files that should be excluded
    excluded_files = set()

    for group in exact_duplicates.values():

        # Prefer keeping the original file instead of a copy
        original = [f for f in group if "- Copy" not in f.stem]

        if original:
            original_file = original[0]
        else:
            original_file = group[0]

        # Exclude the other duplicate files
        for file in group:
            if file != original_file:
                excluded_files.add(file)

    # Keep valid files that are not exact duplicates
    kept_files = [f for f in valid_files if f not in excluded_files]

    # Check whether the folder contains files other than .gitkeep
    existing_files = [
        f for f in cleaned_dir.rglob("*")
        if f.is_file() and f.name != ".gitkeep"
    ]

    if existing_files:
        raise FileExistsError(
            "The cleaned folder already contains files. Please check it first."
        )

    # Create the cleaned folder
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    # Copy the remaining images while keeping their class folders
    for file in kept_files:
        relative_path = file.relative_to(raw_dir)
        destination = cleaned_dir / relative_path

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, destination)

    # Find near-duplicate groups for reporting only
    near_duplicates = find_near_duplicates(kept_files)

    # Return the cleaning results
    return {
        "total": len(files),
        "corrupt": len(files) - len(valid_files),
        "exact_dupes": len(excluded_files),
        "near_dupes": len(near_duplicates),
        "kept": len(kept_files)
    }