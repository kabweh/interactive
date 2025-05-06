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

    # 2) Instantiate the explainer
    explainer = LessonExplainer()

    # 3) Generate the explanation via whichever method exists
    explanation_html = None
    if hasattr(explainer, "explain"):
        # newest API
        explanation_html = explainer.explain(text, level=level)
    elif hasattr(explainer, "generate"):
        # older alias
        explanation_html = explainer.generate(text, level=level)
    elif hasattr(explainer, "generate_explanation"):
        # some versions expect positional args only
        explanation_html = explainer.generate_explanation(text, level)
    elif hasattr(explainer, "get_explanation"):
        # even older API
        explanation_html = explainer.get_explanation(text, level=level)
    else:
        # no supported method found
        st.warning("⚠️ LessonExplainer has no supported explanation method.")
        return

    # 4) Display the HTML with highlights and notes
    st.markdown(explanation_html, unsafe_allow_html=True)
