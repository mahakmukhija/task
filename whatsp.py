import streamlit as st
import datetime
import pywhatkit
import re
import time

# --- Page config ---
st.set_page_config(
    page_title="📱 WhatsApp Message Sender",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for styling ---
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #121212;
        color: #E0E0E0;
    }
    .stButton>button {
        background-color: #25D366;
        color: white;
        font-weight: 600;
        font-size: 18px;
        border-radius: 12px;
        padding: 0.6em 2em;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1ebe57;
        cursor: pointer;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
        background-color: #1E1E1E;
        color: #FFF;
        border: 1px solid #333;
    }
    .stTextInput>div>div>input::placeholder, .stTextArea>div>textarea::placeholder {
        color: #888;
    }
    .stNumberInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
        background-color: #1E1E1E;
        color: #FFF;
        border: 1px solid #333;
        font-size: 16px;
    }
    .stInfo {
        background-color: #333;
        border-radius: 10px;
        padding: 10px;
    }
    .stSuccess {
        background-color: #1e4620;
        border-radius: 10px;
        padding: 10px;
        color: #a6f77b;
    }
    .stError {
        background-color: #462020;
        border-radius: 10px;
        padding: 10px;
        color: #f77b7b;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar inputs ---
with st.sidebar:
    st.header("📥 Message Details")
    phone = st.text_input(
        "📞 Receiver's Phone Number",
        placeholder="+91XXXXXXXXXX",
        help="Include country code, e.g., +919876543210"
    )
    message = st.text_area(
        "💬 Message",
        height=150,
        help="Type your WhatsApp message here."
    )
    st.markdown("### ⏰ Schedule Time")
    col1, col2 = st.columns(2)
    with col1:
        hour = st.number_input(
            "Hour (24h)",
            min_value=0, max_value=23,
            value=datetime.datetime.now().hour
        )
    with col2:
        minute = st.number_input(
            "Minute",
            min_value=0, max_value=59,
            value=(datetime.datetime.now().minute + 1) % 60
        )
    st.markdown("---")

# --- Main area ---
st.title("🤖 Auto WhatsApp Message Sender")
st.markdown("Schedule your WhatsApp messages easily and reliably!")

# Live preview in main area
if message.strip():
    st.subheader("👀 Message Preview")
    st.markdown(f"""
    **To:** `{phone}`  
    **Scheduled for:** {hour:02d}:{minute:02d}  
    **Message:**  
    > {message.replace('\n', '  \n> ')}
    """)

# Schedule button with feedback
if st.button("🚀 Schedule Message"):
    phone_clean = phone.replace("++", "+").replace(" ", "")
    if not re.match(r"^\+\d{12}$", phone_clean):
        st.error("❌ Invalid phone number format. Use format like +919876543210")
    elif not message.strip():
        st.warning("⚠️ Message cannot be empty.")
    else:
        with st.spinner(f"⏳ Scheduling message for {hour:02d}:{minute:02d}..."):
            try:
                pywhatkit.sendwhatmsg(
                    phone_clean, message, int(hour), int(minute),
                    wait_time=10, tab_close=True
                )
                st.success("✅ Message scheduled successfully! Please keep your browser open and logged into WhatsApp Web.")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Failed to schedule message: {e}")

# Footer with badges and social links
st.markdown("---")
col1, col2 = st.columns([1,3])
with col1:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.svg", width=60)
with col2:
    st.markdown("""
    <div style="font-size:14px; color:#888;">
    Made with ❤️ using Streamlit & pywhatkit  
    <br>
    <a href="https://github.com/yourusername/whatsapp-sender" target="_blank" style="color:#25D366;">⭐ Star on GitHub</a> &nbsp;|&nbsp;
    <a href="https://twitter.com/yourhandle" target="_blank" style="color:#25D366;">🐦 Follow on Twitter</a>
    </div>
    """, unsafe_allow_html=True)

