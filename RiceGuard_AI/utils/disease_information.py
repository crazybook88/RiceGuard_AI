"""Decoupled knowledge base. Owner: Member 6.

Keys MUST match settings.CLASS_NAMES. Entries below are PLACEHOLDERS.
TODO (Member 6): write each entry from cited, reputable agronomy sources (e.g. IRRI,
university extension services), list them in `sources`, and keep a disclaimer:
this app is an educational aid, not a substitute for an agronomist.
"""
from __future__ import annotations

from typing import Dict, List, TypedDict


class DiseaseInfo(TypedDict):
    description: str
    symptoms: List[str]
    causes: List[str]
    management: List[str]
    sources: List[str]


DISEASE_INFO: Dict[str, DiseaseInfo] = {
    "Healthy Rice Leaf": {
        "description": "TODO: no visible disease symptoms.",
        "symptoms": ["TODO"], "causes": [], "management": ["TODO"], "sources": [],
    },
    "Bacterial Leaf Blight": {
        "description": "TODO", "symptoms": ["TODO"], "causes": ["TODO"], "management": ["TODO"], "sources": [],
    },
    "Brown Spot": {
        "description": "TODO", "symptoms": ["TODO"], "causes": ["TODO"], "management": ["TODO"], "sources": [],
    },
    "Rice Blast": {
        "description": "TODO", "symptoms": ["TODO"], "causes": ["TODO"], "management": ["TODO"], "sources": [],
    },
}

_FALLBACK: DiseaseInfo = {
    "description": "No information available for this class yet.",
    "symptoms": [], "causes": [], "management": [], "sources": [],
}


def get_disease_info(class_name: str) -> DiseaseInfo:
    return DISEASE_INFO.get(class_name, _FALLBACK)
