# ai_tutor_project/quiz_component.py
import streamlit as st

def show_quiz():
    """
    Renders a simple quiz and returns the user’s answers & score once submitted.
    Returns:
        dict or None: 
          - On submit: {'score': int, 'answers': {...}} 
          - Before submit: None
    """
    st.header("Quiz")

    # Example question – replace/add your own as needed
    q1 = "What is 2 + 2?"
    opts1 = ["1", "2", "3", "4"]
    ans1 = st.radio(q1, opts1, key="q1")

    # You can add more questions similarly, using distinct keys...

    if st.button("Submit Quiz"):
        score = 0
        answers = {"q1": ans1}

        # simple scoring logic – adapt to your real quiz
        if ans1 == "4":
            score += 1

        # feedback
        if score > 0:
            st.success(f"You scored {score} point{'s' if score!=1 else ''}!")
        else:
            st.error("Better luck next time!")

        return {"score": score, "answers": answers}

    return None
