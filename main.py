import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import openai
import io
from gtts import gTTS

openai.api_key = st.secrets.get("OPENAI_API_KEY")  # or your environment variable

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image):
    return image.convert("RGB")

def run_ocr(image):
    result = reader.readtext(np.array(image), detail=0)
    raw_text = " ".join(result)
    return raw_text

def clean_with_gpt(raw_text):
    prompt = (
        "You are an AI assistant specialized in cleaning OCR text from educational images containing counting numbers and numeric sequences. "
        "Please correct any OCR errors, fix misread numbers or words, and output a clean numeric sequence or educational text preserving the counting correctly.\n\n"
        f"Raw OCR text: '''{raw_text}'''\n\n"
        "Output only the corrected, clean text preserving counting sequences."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.1,
    )
    return response['choices'][0]['message']['content'].strip()

st.title("🧠 OCR + AI Counting Cleaner")

uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    preprocessed = preprocess_image(image)

    with st.spinner("Running OCR..."):
        raw_text = run_ocr(preprocessed)
        st.write("Raw OCR output:")
        st.write(raw_text)

    with st.spinner("Cleaning with GPT..."):
        cleaned = clean_with_gpt(raw_text)

    st.subheader("Cleaned Text:")
    st.write(cleaned)

    tts = gTTS(cleaned)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    st.audio(audio_fp.read(), format="audio/mp3")
