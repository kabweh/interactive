import streamlit as st
from lesson_explainer import LessonExplainer


def show_explanation(text: str) -> None:
    """
    Display an interactive explanation interface using LessonExplainer.

    Args:
        text: The extracted lesson material to explain.
    """
    # 1) Choose difficulty level
    level = st.selectbox(
        "Select difficulty level:",
        ["easy", "medium", "hard"],
        index=0
    )

    # 2) Instantiate the explainer (no args)
    explainer = LessonExplainer()

    # 3) Generate the explanation
    explanation_html = explainer.explain(text, level=level)

    # 4) Display the HTML with highlights and notes
    st.markdown(explanation_html, unsafe_allow_html=True)
