# ai_tutor_project/quiz_component.py
import streamlit as st
from quiz_generator import QuizGenerator

def show_quiz(text: str):
    """
    Renders a quiz based on the provided text content.
    """
    st.write("### Quiz Time!")
    if not text:
        st.info("Please upload and explain some material first.")
        return

    # Generate questions
    gen = QuizGenerator()
    questions = gen.generate(text)

    # Display each question with multiple choice options
    for idx, q in enumerate(questions, start=1):
        st.radio(
            label=f"{idx}. {q}",
            options=["A", "B", "C", "D"],
            key=f"quiz_{idx}"
        )
