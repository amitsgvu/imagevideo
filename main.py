import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import io
import re
import easyocr
from gtts import gTTS

# Initialize EasyOCR once
reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image):
    # Convert to grayscale
    image = image.convert("L")
    # Median filter to reduce noise
    image = image.filter(ImageFilter.MedianFilter(size=3))
    # Resize for better OCR accuracy
    image = image.resize((image.width * 2, image.height * 2))
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    return np.array(image)

def clean_text(texts):
    cleaned = []
    for text in texts:
        text = text.strip().lower()
        # Remove unwanted characters
        text = re.sub(r"[^a-z0-9\s]", "", text)
        # Filter very short or empty strings
        if 2 <= len(text) <= 30:
            cleaned.append(text)
    return sorted(set(cleaned))

def extract_text(image_array):
    results = reader.readtext(image_array, detail=0)
    return clean_text(results)

st.title("📚 Educational Image Reader with Audio")

uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Processing image and extracting text..."):
        processed_image = preprocess_image(image)
        texts = extract_text(processed_image)

    if texts:
        final_text = ". ".join(texts).capitalize() + "."
        st.success("Extracted Text:")
        st.write(final_text)

        # Generate audio with gTTS
        tts = gTTS(final_text)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        st.audio(audio_bytes.read(), format="audio/mp3")
    else:
        st.warning("No readable text found in the image.")
