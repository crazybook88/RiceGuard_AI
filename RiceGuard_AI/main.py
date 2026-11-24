"""Streamlit entry point. Run: streamlit run main.py

IMPORTANT: this app must never import training/evaluation code or retrain models.
"""
import streamlit as st

from app import detection, disease_library, history, home
from config import settings

st.set_page_config(page_title="RiceGuard AI", page_icon="🌾", layout="wide")

PAGES = {
    "Home": home.render,
    "Detect": detection.render,
    "Disease Library": disease_library.render,
    "History": history.render,
}

st.sidebar.title("RiceGuard AI")
choice = st.sidebar.radio("Navigate", list(PAGES))
st.session_state["use_mock"] = st.sidebar.toggle(
    "Use mock predictions", value=settings.USE_MOCK_MODEL,
    help="ON = fake predictions for UI development. Turn OFF once a real .keras model exists.")
PAGES[choice]()
