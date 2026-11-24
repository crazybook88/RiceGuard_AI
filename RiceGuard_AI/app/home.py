"""Home page. Owner: Member 5 (UI)."""
import streamlit as st

from config import settings


def render() -> None:
    st.title("🌾 RiceGuard AI")
    st.write("Upload a rice leaf photo to get an AI-based disease classification.")
    st.subheader("Supported categories")
    for name in settings.CLASS_NAMES:
        st.markdown(f"- {name}")
    # TODO (Member 5): add usage steps, photo tips, and an educational-use disclaimer.
