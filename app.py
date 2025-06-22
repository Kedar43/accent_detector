import os
import streamlit as st
from huggingface_hub import login
from utils import process_video_url, explain_accent

hf_token = os.getenv("HF_HUB_TOKEN")
if hf_token:
    login(hf_token)

# Configure Streamlit page settings
st.set_page_config(page_title="English Accent Detector", layout="centered")
st.title("🎤 English Accent Detector (SpeechBrain)")

# Input field for user to enter a video URL
video_url = st.text_input("Paste public video URL (MP4, Loom, etc.):")

if video_url:
    try:
        # Show spinner while processing the video and analyzing accent
        with st.spinner("Processing video and analyzing accent..."):
            accent, confidence = process_video_url(video_url)

        # Display results with confidence scores and explanation
        st.success("Analysis complete!")
        st.markdown(f"### 🗣️ Detected Accent: **{accent}**")
        st.markdown(f"### 📊 Confidence Score: **{float(confidence):.2f}%**")
        st.markdown("---")
        st.markdown("### ℹ️ Accent Explanation")
        st.markdown(explain_accent(accent, confidence))

    except RuntimeError as err:
        # Handle known runtime errors gracefully in the UI
        st.error(f"⚠️ {err}")
    except Exception as err:
        # Catch-all for unexpected errors with generic user message
        st.error("⚠️ An unexpected error occurred. Please check the log file.")
