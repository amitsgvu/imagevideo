import streamlit as st
from PIL import Image
import easyocr
import re
import openai
import os
from gtts import gTTS
import io

# Set your OpenAI API key here or as environment variable
openai.api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image):
    return image.convert("RGB")

def run_ocr(image):
    result = reader.readtext(np.array(image), detail=0)
    raw_text = " ".join(result)
    return raw_text

def clean_with_gpt(raw_text):
    prompt = (
        "You are an AI assistant. "
        "Clean and correct the following OCR output from an educational image, "
        "fix numbers, words, and remove noise. Output clean, well-formatted text:\n\n"
        f"OCR text: '''{raw_text}'''"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": prompt}],
        max_tokens=500,
        temperature=0.1,
    )
    return response['choices'][0]['message']['content'].strip()

st.title("🧠 AI-enhanced OCR with GPT text cleaning")

uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    preprocessed = preprocess_image(image)

    with st.spinner("Running OCR..."):
        raw_text = run_ocr(preprocessed)
        st.write("Raw OCR text:")
        st.write(raw_text)

    with st.spinner("Cleaning text with GPT..."):
        cleaned_text = clean_with_gpt(raw_text)

    st.subheader("Cleaned Text:")
    st.write(cleaned_text)

    # Audio
    tts = gTTS(cleaned_text)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    st.audio(audio_fp.read(), format="audio/mp3")
