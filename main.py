import streamlit as st
from PIL import Image
import numpy as np
import cv2
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
import re
import io
from gtts import gTTS
from spellchecker import SpellChecker

@st.cache_resource(show_spinner=False)
def load_model():
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
    return processor, model

def preprocess_image_cv(image):
    # Convert to numpy
    img = np.array(image.convert("RGB"))
    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    # Convert back to PIL
    pil_img = Image.fromarray(thresh)
    return pil_img

def ocr_image(image, processor, model):
    pixel_values = processor(image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def correct_text(text):
    spell = SpellChecker()
    corrected_words = []
    for word in text.split():
        # Check if number or word
        if word.isnumeric():
            corrected_words.append(word)
        else:
            corrected_words.append(spell.correction(word) or word)
    return " ".join(corrected_words)

st.title("📝 OCR with Enhanced Preprocessing + Spell Correction")

uploaded_file = st.file_uploader("Upload image (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    preprocessed = preprocess_image_cv(image)
    st.image(preprocessed, caption="Preprocessed Image", use_column_width=True)

    processor, model = load_model()
    with st.spinner("Running OCR..."):
        raw_text = ocr_image(preprocessed, processor, model)

    cleaned = clean_text(raw_text)
    corrected = correct_text(cleaned)

    if corrected:
        st.subheader("Extracted and Corrected Text:")
        st.write(corrected)

        tts = gTTS(corrected)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp.read(), format="audio/mp3")
    else:
        st.warning("No readable text found.")
