import streamlit as st
from lesson_explainer import LessonExplainer
import inspect

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

    # 2) Instantiate the explainer
    explainer = LessonExplainer()

    # 3) Determine available explanation method
    if hasattr(explainer, "explain"):
        method = explainer.explain
    elif hasattr(explainer, "generate"):
        method = explainer.generate
    elif hasattr(explainer, "generate_explanation"):
        method = explainer.generate_explanation
    elif hasattr(explainer, "get_explanation"):
        method = explainer.get_explanation
    else:
        st.error("Unsupported explainer API. Unable to find an explanation method.")
        return

    # 4) Generate the explanation, with or without difficulty level
    try:
        sig = inspect.signature(method)
        if "level" in sig.parameters:
            explanation_html = method(text, level=level)
        else:
            explanation_html = method(text)
    except Exception as e:
        st.error(f"Error generating explanation: {e}")
        return

    # 5) Display the HTML with highlights and notes
    st.markdown(explanation_html, unsafe_allow_html=True)
