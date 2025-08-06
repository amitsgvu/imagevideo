import streamlit as st
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
import re
import io
from gtts import gTTS

@st.cache_resource(show_spinner=False)
def load_model():
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
    return processor, model

def preprocess_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image

def ocr_image(image, processor, model):
    pixel_values = processor(image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

st.title("📝 Clean OCR with TrOCR + Audio")

uploaded_file = st.file_uploader("Upload image (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    preprocessed = preprocess_image(image)

    processor, model = load_model()
    with st.spinner("Running OCR..."):
        raw_text = ocr_image(preprocessed, processor, model)

    cleaned = clean_text(raw_text)

    if cleaned:
        st.subheader("Extracted Clean Text:")
        st.write(cleaned)

        tts = gTTS(cleaned)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp.read(), format="audio/mp3")
    else:
        st.warning("No readable text found.")
