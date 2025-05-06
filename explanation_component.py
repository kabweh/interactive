import streamlit as st
from lesson_explainer import LessonExplainer

def show_explanation(text):
    """
    Displays the explanation interface: lets the user pick a difficulty level
    and then uses LessonExplainer to generate and render the annotated explanation.
    """
    st.title("Explain")
    # 1) Let the user choose an explanation difficulty
    level = st.selectbox(
        "Select difficulty level:",
        ["easy", "medium", "hard"],
        index=0,
        help="How detailed/challenging should the explanation be?"
    )

    # 2) Instantiate the explainer (pass your Manus API key as positional)
    api_key = st.secrets.get("MANUS_API_KEY")
    explainer = LessonExplainer(api_key)

    # 3) Generate and display the explanation
    resp = explainer.explain(text, level=level)
    st.markdown(resp, unsafe_allow_html=True)
