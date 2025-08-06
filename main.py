import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import io
import re
import pytesseract
from gtts import gTTS

def preprocess_image(image):
    image = image.convert("L")
    image = image.filter(ImageFilter.MedianFilter(3))
    image = image.resize((image.width * 2, image.height * 2))
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    return image

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    lines = [line.strip() for line in text.split('\n') if 2 <= len(line.strip()) <= 30]
    return sorted(set(lines))

st.title("📚 Educational Image Reader with Tesseract OCR + Audio")

uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    preprocessed = preprocess_image(image)

    with st.spinner("Extracting text..."):
        text = pytesseract.image_to_string(preprocessed)

    cleaned = clean_text(text)

    if cleaned:
        final_text = ". ".join(cleaned).capitalize() + "."
        st.success("Extracted Text:")
        st.write(final_text)

        tts = gTTS(final_text)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp.read(), format="audio/mp3")
    else:
        st.warning("No readable text found.")
