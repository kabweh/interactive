# ai_tutor_project/report_component.py
import streamlit as st
from report_generator import build_report
import smtplib
from email.message import EmailMessage

def send_report():
    """
    Generates and emails the progress report PDF to parents.
    """
    # Ensure user is logged in
    user = st.session_state.get("user")
    if not user:
        st.error("Please log in to send a report.")
        return

    # Build the PDF report
    try:
        pdf_bytes = build_report(user)
    except Exception as e:
        st.error(f"Error building report: {e}")
        return

    # Compose the email
    msg = EmailMessage()
    msg["Subject"] = "Your Child's Progress Report"
    msg["From"] = st.secrets["email"]["sender"]
    msg["To"] = ",".join(st.secrets["email"]["parents"])
    msg.set_content("Attached is the latest progress report.")
    msg.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename="progress_report.pdf"
    )

    # Send via SMTP
    try:
        server = st.secrets["email"].get("smtp_server", "smtp.gmail.com")
        port = st.secrets["email"].get("smtp_port", 587)
        user_auth = st.secrets["email"]["user"]
        pass_auth = st.secrets["email"]["pass"]

        with smtplib.SMTP(server, port) as smtp:
            smtp.starttls()
            smtp.login(user_auth, pass_auth)
            smtp.send_message(msg)
        st.success("Progress report emailed successfully!")
    except Exception as e:
        st.error(f"Failed to send report: {e}")
