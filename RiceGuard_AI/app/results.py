"""Result card. Owner: Member 5."""
from typing import Dict

import streamlit as st

from config import settings
from utils.disease_information import get_disease_info


def render_result(result: Dict) -> None:
    if result["is_mock"]:
        st.warning("DEMO RESULT (mock model) - not a real diagnosis.")
    st.subheader(f"Prediction: {result['predicted_class']}")
    st.metric("Confidence", f"{result['confidence']:.1%}")
    if result["is_low_confidence"]:
        st.warning(f"Low confidence (< {settings.CONFIDENCE_THRESHOLD:.0%}). "
                   "Try a clearer, well-lit, close-up photo.")
    st.markdown("**Probability distribution**")
    for name, p in sorted(result["probabilities"].items(), key=lambda kv: -kv[1]):
        st.progress(float(p), text=f"{name}: {p:.1%}")

    info = get_disease_info(result["predicted_class"])
    with st.expander("Disease information", expanded=True):
        st.write(info["description"])
        for title, key in (("Symptoms", "symptoms"), ("Causes", "causes"), ("Management", "management")):
            if info[key]:
                st.markdown(f"**{title}**")
                for item in info[key]:
                    st.markdown(f"- {item}")
    # TODO (Member 5): improve layout (columns/tabs), add a bar chart of probabilities.
