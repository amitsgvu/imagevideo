import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import openai
import io
from gtts import gTTS

openai.api_key = st.secrets.get("OPENAI_API_KEY")  # Or set your env variable

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image):
    return image.convert("RGB")

def run_ocr(image):
    result = reader.readtext(np.array(image), detail=0)
    raw_text = " ".join(result)
    return raw_text

def clean_with_gpt(raw_text):
    prompt = f"""
You are an expert at reading and correcting text extracted by OCR from educational images containing counting sequences.

The OCR text is noisy and may have errors or irrelevant fragments, but you know the image only contains counting numbers from 1 to 10.

Your job: 
- Extract the counting sequence from 1 to 10 in correct order.
- Correct OCR mistakes (e.g., 'ten ga' → '10').
- Ignore any noise or irrelevant text.
- Output the cleaned counting sequence as: "1 2 3 4 5 6 7 8 9 10".

Here is the raw OCR text: 
'''{raw_text}'''

Provide ONLY the cleaned counting sequence.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.0,
    )
    return response['choices'][0]['message']['content'].strip()

st.title("Counting OCR Cleaner — Human-Level Understanding")

uploaded_file = st.file_uploader("Upload counting image", type=["png", "jpg", "jpeg"])

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

    st.subheader("Cleaned Counting Sequence:")
    st.write(cleaned)

    tts = gTTS(cleaned)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    st.audio(audio_fp.read(), format="audio/mp3")
