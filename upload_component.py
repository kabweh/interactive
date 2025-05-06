import streamlit as st
from lesson_explainer import LessonExplainer


def show_explanation(text: str) -> None:
    """
    Display an interactive explanation of provided lesson text.
    """
    # 1) Ask user for difficulty level
    level = st.selectbox(
        "Select difficulty level:",
        ["easy", "medium", "hard"],
        index=0,
    )

    # 2) Instantiate the explainer with API key as a positional argument
    api_key = st.secrets.get("MANUS_API_KEY")
    explainer = LessonExplainer(api_key)

    # 3) Generate explanation
    explanation_html = explainer.explain(text, level=level)

    # 4) Display the rendered HTML explanation
    st.markdown(explanation_html, unsafe_allow_html=True)
