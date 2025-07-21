import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np

# Function to apply various digital effects
def apply_effect(frame, effect):
    if effect == "Pencil Sketch":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        inv_blur = 255 - blur
        sketch = cv2.divide(gray, inv_blur, scale=256.0)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    elif effect == "Cartoon":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon

    elif effect == "Stylized":
        return cv2.stylization(frame, sigma_s=60, sigma_r=0.5)

    elif effect == "Edge Detection":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    else:
        return frame

# Streamlit App UI
st.title("🎨 Real-Time Digital Effects with Webcam")

effect = st.selectbox("🪄 Choose a Digital Effect:", [
    "Pencil Sketch", "Cartoon", "Stylized", "Edge Detection"
])

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame = None

    def transform(self, frame):
        self.frame = frame.to_ndarray(format="bgr24")
        return apply_effect(self.frame, effect)

webrtc_ctx = webrtc_streamer(
    key="digital_effects",
    desired_playing_state=True,
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
    async_transform=True,
)

# Image capture and download
if "captured" not in st.session_state:
    st.session_state.captured = False

if webrtc_ctx.video_transformer:
    if st.button("📸 Capture Image with Effect"):
        frame = webrtc_ctx.video_transformer.frame
        if frame is not None:
            processed = apply_effect(frame, effect)
            filename = f"captured_{effect.replace(' ', '_').lower()}.jpg"
            cv2.imwrite(filename, processed)
            st.image(processed, channels="BGR", caption=f"🖼️ {effect}")
            st.success(f"✅ Saved as {filename}")
            st.session_state.captured = True
        else:
            st.warning("⚠️ Waiting for webcam frame...")

if st.session_state.captured:
    with open(filename, "rb") as file:
        st.download_button("⬇️ Download", file, file.name, "image/jpeg")
