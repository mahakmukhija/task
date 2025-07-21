import streamlit as st
from twilio.rest import Client

st.set_page_config(page_title="WhatsApp Sender", layout="centered")
st.title("💬 Send WhatsApp Message using Twilio")

st.info("You must use the Twilio sandbox number: +14155238886 and join the sandbox from your phone.")

# Input credentials
account_sid = st.text_input("🔐 Twilio Account SID", type="password")
auth_token = st.text_input("🔑 Twilio Auth Token", type="password")

# Input numbers and message
receiver_number = st.text_input("📱 Receiver WhatsApp Number (with country code)", placeholder="+919999999999")
message_body = st.text_area("✉️ Message to send", placeholder="Hi there!")

if st.button("🚀 Send Message"):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_="whatsapp:+14155238886",  # Twilio Sandbox number
            to=f"whatsapp:{receiver_number}"
        )
        st.success(f"✅ Message sent! SID: {message.sid}")
    except Exception as e:
        st.error(f"❌ Failed to send message: {e}")
