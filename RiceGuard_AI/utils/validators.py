"""Upload validation for Streamlit UploadedFile objects. Owner: Member 5."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image, UnidentifiedImageError

from config import settings


@dataclass
class ValidationResult:
    ok: bool
    message: str = ""
    image: Optional[Image.Image] = None


def validate_uploaded_file(uploaded_file) -> ValidationResult:
    """Check extension, non-empty, size, PIL readability and channels."""
    ext = Path(uploaded_file.name).suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        return ValidationResult(False, f"Unsupported file type '{ext}'.")
    data = uploaded_file.getvalue()
    if len(data) == 0:
        return ValidationResult(False, "The file is empty.")
    if len(data) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        return ValidationResult(False, f"File exceeds {settings.MAX_FILE_SIZE_MB} MB.")
    try:
        uploaded_file.seek(0)
        Image.open(uploaded_file).verify()
        uploaded_file.seek(0)
        img = Image.open(uploaded_file)
        img.load()
    except (UnidentifiedImageError, OSError):
        return ValidationResult(False, "The file is not a readable image.")
    # TODO (Member 5): decide + document which PIL modes are accepted (e.g. is 1-channel
    # 'L' OK?) and add a minimum-dimension check.
    return ValidationResult(True, "OK", img)
