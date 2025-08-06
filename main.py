import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
import requests
import io
import base64

st.set_page_config(page_title="Image to Video Generator", layout="centered")
st.title("🖼️🔊➡️🎞️ Image to Video (Open Source Pipeline)")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # OCR Extraction
    st.subheader("📖 Extracted Text")
    image = Image.open(uploaded_file)
    extracted_text = pytesseract.image_to_string(image)
    st.write(extracted_text.strip() or "No text detected.")

    # Audio Generation
    st.subheader("🔈 Generated Audio")
    tts = gTTS(text=extracted_text or "No text detected", lang="en")
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    st.audio(audio_buffer, format="audio/mp3")

    # Send image to video generation API
    st.subheader("🎥 Generated Video")
