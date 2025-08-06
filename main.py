import streamlit as st
from PIL import Image, ImageEnhance
import easyocr
import numpy as np
import io
from gtts import gTTS
import re

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image):
    # Enhance image contrast for better OCR
    image = image.convert("L")
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    return image

def run_ocr(image):
    results = reader.readtext(np.array(image), detail=0)
    return results

def normalize_text(text):
    # Normalize OCR text to numbers 1-10 with some known corrections
    corrections = {
        'one': '1', 'two': '2', 'three': '3', 'four': '4',
        'five': '5', 'six': '6', 'seven': '7', 'eight': '8',
        'nine': '9', 'ten': '10', 'to': '2', 'lo': '10', '0': '0'
    }
    text = text.lower()
    for k, v in corrections.items():
        text = re.sub(r'\b'+k+r'\b', v, text)
    # Remove non-digit and non-space characters
    text = re.sub(r'[^0-9\s]', ' ', text)
    # Collapse multiple spaces to one
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_numbers(text):
    # Extract list of integers from text
    nums = re.findall(r'\b\d+\b', text)
    return [int(n) for n in nums if 1 <= int(n) <= 10]

def validate_counting(numbers):
    # Validate counting sequence from 1 to 10 in order, allow missing but warn if totally wrong
    expected = list(range(1, 11))
    matched = [n for n in numbers if n in expected]
    if not matched:
        return None  # No valid numbers found
    # Check order and coverage
    if all(x <= y for x, y in zip(matched, matched[1:])):
        return matched
    return None

st.title("Accurate Counting 1 to 10 Extractor")

uploaded_file = st.file_uploader("Upload an image with counting 1 to 10", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    preprocessed = preprocess_image(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Running OCR..."):
        raw_results = run_ocr(preprocessed)
        raw_text = " ".join(raw_results)
        st.write("Raw OCR output:")
        st.write(raw_text)

    normalized = normalize_text(raw_text)
    st.write("Normalized text (converted to numbers):")
    st.write(normalized)

    numbers = extract_numbers(normalized)
    st.write("Extracted numbers:")
    st.write(numbers)

    validated = validate_counting(numbers)
    if validated:
        final_text = " ".join(str(n) for n in validated)
        st.success("Cleaned counting sequence (1 to 10):")
        st.write(final_text)

        # Generate audio
        tts = gTTS(final_text)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp.read(), format="audio/mp3")
    else:
        st.error("Could not reliably extract counting from 1 to 10. Please try a clearer image.")
