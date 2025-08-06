import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import io
import re
import pytesseract
from gtts import gTTS

def preprocess_image(image):
    # Grayscale
    image = image.convert("L")

    # Resize (scale up)
    image = image.resize((image.width * 3, image.height * 3), Image.LANCZOS)

    # Sharpen image
    image = image.filter(ImageFilter.SHARPEN)

    # Adaptive thresholding (binarize)
    image = ImageOps.autocontrast(image)
    image = image.point(lambda x: 0 if x < 140 else 255, mode='1')

    return image

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    lines = [line.strip() for line in text.split('\n') if 2 <= len(line.strip()) <= 30]
    return sorted(set(lines))

st.title("📚 Enhanced Educational Image Reader with Tesseract OCR + Audio")

uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    preprocessed = preprocess_image(image)
    st.image(preprocessed, caption="Preprocessed Image", use_column_width=True)

    with st.spinner("Extracting text..."):
        # Use config options for better recognition
        config = "--oem 3 --psm 6"
        text = pytesseract.image_to_string(preprocessed, config=config)

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
