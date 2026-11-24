"""Disease library page. Owner: Member 6."""
import streamlit as st

from config import settings
from utils.disease_information import get_disease_info


def render() -> None:
    st.header("Disease library")
    for name in settings.CLASS_NAMES:
        info = get_disease_info(name)
        with st.expander(name):
            st.write(info["description"])
            # TODO (Member 6): show symptoms/causes/management/sources + reference images
            # (only images you have the right to use; credit them).
