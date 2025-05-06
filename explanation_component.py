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

    # 3) Generate the explanation by trying known methods and calling them flexibly
    explanation_html = None
    for method_name in ("explain", "generate", "generate_explanation", "get_explanation"):
        if hasattr(explainer, method_name):
            method = getattr(explainer, method_name)
            # Try calling with level as keyword, then positional, then without
            for call in (
                lambda: method(text, level=level),
                lambda: method(text, level),
                lambda: method(text),
            ):
                try:
                    explanation_html = call()
                    break
                except TypeError:
                    continue
            if explanation_html is not None:
                break

    if explanation_html is None:
        raise AttributeError(
            "Could not call any of explain/generate/generate_explanation/get_explanation "
            "with or without a 'level' argument on LessonExplainer."
        )

    # 4) Display the HTML with highlights and notes
    st.markdown(explanation_html, unsafe_allow_html=True)
