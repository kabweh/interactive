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

    # 3) Generate the explanation by trying a few likely method names
    if hasattr(explainer, "generate"):
        explanation_html = explainer.generate(text, level=level)
    elif hasattr(explainer, "generate_explanation"):
        explanation_html = explainer.generate_explanation(text, level=level)
    elif hasattr(explainer, "get_explanation"):
        explanation_html = explainer.get_explanation(text, level=level)
    else:
        raise AttributeError(
            "LessonExplainer has no `.generate`, "
            "`.generate_explanation` or `.get_explanation` method. "
            "Please update this file to call the correct method name."
        )

    # 4) Display the HTML with highlights and notes
    st.markdown(explanation_html, unsafe_allow_html=True)
