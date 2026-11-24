"""Upload -> validate -> preview -> predict. Owner: Member 5 (UI) + Member 4 (logic)."""
import streamlit as st

from app import results
from model.predict import predict_image
from utils import history_manager
from utils.validators import validate_uploaded_file


def render() -> None:
    st.header("Detect disease")
    use_mock = st.session_state.get("use_mock", True)
    if use_mock:
        st.info("Mock mode is ON: predictions are FAKE and for UI testing only.")

    uploaded = st.file_uploader("Upload a rice leaf image", type=["jpg", "jpeg", "png"])
    if uploaded is None:
        return

    check = validate_uploaded_file(uploaded)
    if not check.ok:
        st.error(check.message)
        return

    st.image(check.image, caption="Uploaded image", use_container_width=True)

    if st.button("Analyse image", type="primary"):
        try:
            with st.spinner("Analysing..."):
                result = predict_image(check.image, use_mock=use_mock)
        except (NotImplementedError, FileNotFoundError) as exc:
            st.error(f"Real model is not ready yet ({exc!r}). Turn on mock mode in the sidebar.")
            return
        history_manager.append_record(uploaded.name, result)
        results.render_result(result)
    # TODO (Member 5): keep the result visible after reruns via st.session_state.
