import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import os
import requests

# Set page config
st.set_page_config(page_title="Kid Learning Video Creator", layout="centered")

st.title("📚🧠 AI Learning Video Creator for Kids")
st.write("Upload a chapter image, and get a narrated video for your kid to learn easily.")

# Upload image
uploaded_file = st.file_uploader("Upload a chapter image (PNG or JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    image = Image.open(uploaded_file)

    # Extract text using pytesseract
    extracted_text = pytesseract.image_to_string(image)
    st.subheader("📖 Extracted Text")
    st.text(extracted_text)

    # Call local Ollama model to summarize for a child
    with st.spinner("👶 Creating kid-friendly explanation using AI..."):
        prompt = f"Explain the following to a child in 1st grade using simple words:\n\n{extracted_text}"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        ai_summary = response.json()["response"]
        st.subheader("🧠 AI Summary for Kids")
        st.write(ai_summary)

        # Generate speech using gTTS
        tts = gTTS(ai_summary)
        audio_path = "output_audio.mp3"
        tts.save(audio_path)

        # Create video with image and audio
        st.subheader("🎞️ Final Learning Video")
        image_clip = ImageClip(uploaded_file).set_duration(10)
        audio_clip = AudioFileClip(audio_path)
        final_video = image_clip.set_audio(audio_clip)
        video_path = "learning_video.mp4"
        final_video.write_videofile(video_path, fps=24)

        st.video(video_path)

        # Cleanup
        image_clip.close()
        audio_clip.close()
        os.remove(audio_path)
