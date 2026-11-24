"""History page. Owner: Member 5."""
import streamlit as st

from utils import history_manager


def render() -> None:
    st.header("Detection history")
    df = history_manager.read_history()
    if df.empty:
        st.info("No detections recorded yet.")
        return
    st.dataframe(df, use_container_width=True)
    st.download_button("Export CSV", df.to_csv(index=False), "detection_history.csv", "text/csv")
    if st.button("Clear history"):
        history_manager.clear_history()
        st.rerun()
    # TODO (Member 5): filter by class/date; add a confirmation step before clearing.
