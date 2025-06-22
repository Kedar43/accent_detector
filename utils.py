import os
import uuid
import logging
import requests
import traceback
import streamlit as st
from moviepy.video.io.VideoFileClip import VideoFileClip
from speechbrain.pretrained.interfaces import foreign_class

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def download_file(video_url):
    """
    Download a file from a URL and save it as a temporary file.

    Args:
        url (str): The URL to download from.

    Returns:
        str: Path to the downloaded temporary file.
    """
    try:
        video_id = str(uuid.uuid4())
        video_filename = os.path.join(os.getcwd(), f"{video_id}_video.mp4")
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(video_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        logging.info(f"Downloaded video to {video_filename}")
        return video_filename
    except Exception as e:
        logging.error(f"Error downloading video: {e}\n{traceback.format_exc()}")
        raise RuntimeError("Failed to download the video. Please try another video.")
    
def extract_audio(video_path):
    """
    Extract up to 60 seconds of audio from the input video file.
    Saves the extracted audio as a temporary .wav file.

    Args:
        video_path (str): Path to the input video file.

    Returns:
        str: Path to the extracted audio file.
    """
    try:
        video = VideoFileClip(video_path)
        audio_duration = min(video.audio.duration, 60)
        trimmed_audio = video.audio.subclipped(0, audio_duration)
        audio_id = str(uuid.uuid4())
        audio_filename = os.path.join(os.getcwd(), f"{audio_id}_audio.wav")
        trimmed_audio.write_audiofile(audio_filename, codec='pcm_s16le', logger=None)
        logging.info(f"Extracted audio to {audio_filename}")
        return audio_filename
    except Exception as e:
        logging.error(f"Error extracting audio: {e}\n{traceback.format_exc()}")
        raise RuntimeError("Sorry, we could not extract audio from the video. Please try another video.")

@st.cache_resource(show_spinner=False)
def load_classifier():
    """
    Load the SpeechBrain accent classification model.

    Returns:
        foreign_class instance: Loaded classifier object.
    """
    try:
        classifier = foreign_class(
            source="Jzuluaga/accent-id-commonaccent_xlsr-en-english",
            pymodule_file="custom_interface.py",
            classname="CustomEncoderWav2vec2Classifier"
        )
        logging.info("Loaded SpeechBrain accent classifier")
        return classifier
    except Exception as e:
        logging.error(f"Error loading SpeechBrain classifier: {e}\n{traceback.format_exc()}")
        raise RuntimeError("Failed to load the Classifier. Please try again later.")

def classify_accent(classifier, audio_path):
    """
    Classify the English accent from the given audio file using the loaded classifier.

    Args:
        classifier (foreign_class): The loaded SpeechBrain classifier.
        audio_path (str): Path to the audio file.

    Returns:
        tuple: (accent label (str), confidence score (float))
    """
    try:
        out_prob, score, index, text_lab = classifier.classify_file(audio_path)
        logging.info(f"Classified accent: {text_lab} with confidence {float(score)*100:.2f}%")
        return text_lab, score * 100
    except Exception as e:
        logging.error(f"Error classifying accent: {e}\n{traceback.format_exc()}")
        raise RuntimeError("The accent model failed to load. Please try again later.")

def explain_accent(accent, confidence):
    """
    Generate a human-readable explanation for the detected accent and confidence score.

    Args:
        accent (str): Detected accent label.
        confidence (float): Confidence score (percentage).

    Returns:
        str: Explanation markdown string.
    """
    return f"""
        The system detected a **{accent}** English accent with **{float(confidence):.2f}% confidence**.  
        This score reflects how closely your voice matches typical speech patterns of native {accent} English speakers based on pronunciation, rhythm, and intonation.

        The model analyzes vocal features using a neural network trained on speakers with known accents. While it can differentiate between major English accents, its accuracy may vary with noisy audio, strong regional variation, or non-native speakers.
    """

def process_video_url(video_url):
    """
    End-to-end processing of the video URL:
    - Download video file
    - Extract audio (up to 60 seconds)
    - Load classifier model
    - Classify the accent
    - Cleanup temporary files

    Args:
        video_url (str): URL of the public video file.

    Returns:
        tuple: (accent label (str), confidence score (float))
    """
    video_path = None
    audio_path = None

    try:
        video_path = download_file(video_url)
        audio_path = extract_audio(video_path)

        classifier = load_classifier()
        accent, confidence = classify_accent(classifier, audio_path)

        return accent[0].upper(), confidence

    finally:
        # Clean up temporary files if they exist
        for path in [audio_path, video_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                    logging.info(f"Removed temporary file: {path}")
                except Exception as e:
                    logging.warning(f"Failed to remove temp file {path}: {e}")