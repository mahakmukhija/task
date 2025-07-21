import streamlit as st
import requests

st.set_page_config(page_title="Anonymous Email Sender", layout="centered")
st.title("📧 Send Email Without Revealing Your Email ID (Using SendGrid)")

to_email = st.text_input("Recipient Email")
subject = st.text_input("Subject")
body = st.text_area("Email Body")
sendgrid_api_key = st.text_input("SendGrid API Key", type="password")
from_email = st.text_input("From Email (Verified SendGrid sender)")

if st.button("Send Email"):
    if not all([to_email, subject, body, sendgrid_api_key, from_email]):
        st.error("Please fill in all fields!")
    else:
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {sendgrid_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "personalizations": [
                {"to": [{"email": to_email}]}
            ],
            "from": {"email": from_email},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 202:
            st.success("✅ Email sent successfully!")
        else:
            st.error(f"❌ Failed to send email: {response.text}")
