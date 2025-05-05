# ai_tutor_project/report_component.py
import streamlit as st
from report_generator import build_report
import smtplib
from email.message import EmailMessage

def send_report():
    """
    Generates the PDF report for the current user and emails it to the configured parent addresses.
    """
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("User ID not found. Please log in before sending a report.")
        return

    # Build the PDF report
    pdf_bytes = build_report(user_id)

    # Compose the email message
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

    # Send the email via SMTP
    try:
        with smtplib.SMTP(st.secrets["email"]["smtp_server"], port=587) as smtp:
            smtp.starttls()
            smtp.login(
                st.secrets["email"]["user"],
                st.secrets["email"]["pass"]
            )
            smtp.send_message(msg)
        st.success("Progress report emailed successfully!")
    except Exception as e:
        st.error(f"Failed to send report: {e}")
