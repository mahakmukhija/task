import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page setup
st.set_page_config(page_title="📧 Python Email Sender", layout="centered")
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 10px;
        }
        .stTextArea>div>textarea {
            border-radius: 10px;
            padding: 10px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            padding: 0.75rem 2rem;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📨Email Sender")
st.caption("Securely send an email using SMTP with Gmail and Streamlit.")

# 🎯 Input Fields
with st.form("email_form"):
    sender = st.text_input("📤 Sender Email", placeholder="your_email@gmail.com")
    receiver = st.text_input("📥 Receiver Email", placeholder="recipient@gmail.com")
    subject = st.text_input("📝 Subject", placeholder="Your subject here...")
    body = st.text_area("💬 Email Body", placeholder="Type your message here...", height=150)
    app_password = st.text_input("🔐 App Password (Gmail, 16-digit)", type="password")

    submit = st.form_submit_button("🚀 Send Email")

# 🚀 Sending logic
if submit:
    if not sender or not receiver or not app_password or not subject or not body:
        st.warning("⚠️ Please fill in all fields.")
    else:
        try:
            # Construct MIME email
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = receiver
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Connect to Gmail SMTP
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, app_password)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()

            st.success("✅ Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
