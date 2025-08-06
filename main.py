import streamlit as st
import easyocr
from PIL import Image, ImageEnhance
import numpy as np
import re
from gtts import gTTS
import io

# Image preprocessing
def preprocess_image(image):
    image = image.convert("RGB")
    image = image.resize((image.width * 2, image.height * 2))  # upscale for clarity
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # increase contrast
    return image

# Clean and filter text
def clean_text(results):
    cleaned = []
    for text in results:
        text = text.strip().lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # remove special chars
        if 2 <= len(text) <= 15 and re.search(r"[a-zA-Z0-9]", text):  # filter short/junk
            cleaned.append(text)
    return sorted(set(cleaned))

# OCR + cleaning
def extract_text(image):
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(np.array(image), detail=0)
    return clean_text(results)

# Streamlit app
st.title("📚 AI Educational Image Reader")
uploaded_file = st.file_uploader("Upload an educational image (e.g., numbers, ABCs, charts)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    preprocessed_image = preprocess_image(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Reading and cleaning text..."):
        clean_results = extract_text(preprocessed_image)

    if clean_results:
        final_text = ". ".join(clean_results).capitalize() + "."
        st.success("✅ Clean text extracted:")
        st.write(final_text)

        # Generate and play audio
        tts = gTTS(final_text)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp.read(), format="audio/mp3")
    else:
