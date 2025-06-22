# English Accent Detector (SpeechBrain)

This Streamlit app detects English accents from speech in public video URLs using the SpeechBrain accent classification model.

---

## Features

- Input a public video URL (MP4, Loom, etc.)
- Downloads the video
- Extracts up to 60 seconds of audio
- Classifies English accent with confidence score
- Provides an explanation of the detected accent

---

## Requirements

- Python 3.12 or higher
- ffmpeg installed and available in PATH (required by `moviepy`)
- Internet connection (to download videos and model weights)

---

## Setup

1. **Clone the repo** (or copy your project files):

    ```bash
    git clone https://github.com/Kedar43/accent_detector.git
    cd accent_detector
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

- This will open a browser window/tab with the app interface.
- Paste a public video URL (must be MP4).
- Wait while the app downloads the video and processes audio (up to 60 seconds).
- View the detected English accent, confidence score, and explanation.

---

## Testing the app
- Use sample public MP4 videos containing English speech with distinct accents.
- The app logs runtime info and errors to app.log in the working directory.
- If errors occur, check app.log for detailed traceback and messages.

---

## Notes
- The SpeechBrain model is loaded once and cached to improve performance on repeated runs.
- Temporary video and audio files are deleted automatically after processing.
- Accuracy depends on the quality of audio and the SpeechBrain model’s training data.
- Make sure video URLs are publicly accessible without authentication.