"""CSV detection history. Owner: Member 5. All functions take an optional path
so tests can use a temp file."""
from __future__ import annotations

import threading
from datetime import datetime
from pathlib import Path
from typing import Dict

import pandas as pd

from config import settings

HISTORY_COLUMNS = ["timestamp", "filename", "predicted_class", "confidence", "is_low_confidence", "is_mock"]
_lock = threading.Lock()


def read_history(path: Path = settings.HISTORY_CSV) -> pd.DataFrame:
    """Return history as a DataFrame; empty (with correct columns) if missing/corrupt."""
    if not Path(path).exists():
        return pd.DataFrame(columns=HISTORY_COLUMNS)
    try:
        df = pd.read_csv(path)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=HISTORY_COLUMNS)
    # TODO (Member 5): stricter schema validation (missing/extra columns -> backup + reset).
    return df.reindex(columns=HISTORY_COLUMNS)


def append_record(filename: str, result: Dict, path: Path = settings.HISTORY_CSV) -> None:
    """Append one prediction (output of predict_image) to the CSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "filename": filename,
        "predicted_class": result["predicted_class"],
        "confidence": round(result["confidence"], 4),
        "is_low_confidence": result["is_low_confidence"],
        "is_mock": result["is_mock"],
    }
    with _lock:
        pd.DataFrame([row], columns=HISTORY_COLUMNS).to_csv(
            path, mode="a", header=not path.exists(), index=False)


def clear_history(path: Path = settings.HISTORY_CSV) -> None:
    """Delete all records."""
    with _lock:
        Path(path).unlink(missing_ok=True)
