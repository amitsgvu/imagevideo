import streamlit as st
from PIL import Image, ImageEnhance
import easyocr
import numpy as np
import io
from gtts import gTTS
import openai
import re

# Setup your OpenAI API key (put your key in Streamlit secrets or environment)
openai.api_key = st.secrets.get("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY"

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image):
    image = image.convert("L")
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    return image

def run_ocr(image):
    results = reader.readtext(np.array(image), detail=0)
    return " ".join(results)

def clean_text_with_ai(raw_text, context="counting 1 to 10"):
    prompt = f"""
You are a helpful assistant that receives noisy OCR text extracted from educational images.

The text is about "{context}". Your job is to understand the content and clean it up into correct, human-readable text.

Here is the OCR text:
\"\"\"{raw_text}\"\"\"

Clean and correct the text accordingly and return only the cleaned content.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()

st.title("AI-powered Educational OCR Cleaner")

uploaded_file = st.file_uploader("Upload your educational image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    preprocessed = preprocess_image(image)
    with st.spinner("Running OCR..."):
        raw_text = run_ocr(preprocessed)
        st.write("Raw OCR output:")
        st.write(raw_text)

    with st.spinner("Cleaning OCR text with AI..."):
        cleaned_text = clean_text_with_ai(raw_text, context="counting from 1 to 10")
        st.success("Cleaned text:")
        st.write(cleaned_text)

    # Convert to speech
    if cleaned_text:
        tts = gTTS(cleaned_text)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp.read(), format="audio/mp3")
