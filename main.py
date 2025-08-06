import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import requests
import io
import openai

OCR_SPACE_URL = "https://api.ocr.space/parse/image"

# Preprocess: grayscale, enhance contrast, binarize
def preprocess_image(image):
    image = image.convert("L")  # grayscale
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(3.0)
    image = image.filter(ImageFilter.MedianFilter(size=3))
    # Binarize
    threshold = 140
    image = image.point(lambda p: 255 if p > threshold else 0)
    return image

def ocr_space_api(image_bytes, api_key):
    payload = {'apikey': api_key, 'language': 'eng', 'isOverlayRequired': False}
    files = {'file': ('image.png', image_bytes)}
    response = requests.post(OCR_SPACE_URL, data=payload, files=files)
    result = response.json()
    if result.get("IsErroredOnProcessing"):
        st.error("OCR Error: " + result.get("ErrorMessage", ["Unknown"])[0])
        return ""
    parsed_results = result.get("ParsedResults")
    if parsed_results:
        return parsed_results[0].get("ParsedText", "").strip()
    return ""

def correct_text_with_gpt(text, openai_api_key):
    openai.api_key = openai_api_key
    prompt = (
        "You are a helpful assistant. Correct and clean the following OCR output, "
        "assuming it contains counting numbers from 1 to 10 and related educational text. "
        "Fix errors and return clean, human-readable text only.\n\n"
        f"OCR Output:\n{text}\n\nCorrected Text:"
    )
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0
    )
    return response.choices[0].text.strip()

st.title("📚 OCR + AI Text Cleaner for Educational Images")

uploaded_file = st.file_uploader("Upload image (1-10 counting, ABCs, charts)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    preprocessed = preprocess_image(image)

    st.image(image, caption="Original Image", use_column_width=True)
    st.image(preprocessed, caption="Preprocessed Image (binarized)", use_column_width=True)

    ocr_api_key = st.text_input("Enter your OCR.Space API key", type="password")
    openai_api_key = st.text_input("Enter your OpenAI API key (for text correction)", type="password")

    if st.button("Extract and Correct Text"):
        if not ocr_api_key or not openai_api_key:
            st.warning("Please enter both OCR.Space and OpenAI API keys.")
        else:
            with st.spinner("Running OCR..."):
                img_byte_arr = io.BytesIO()
                preprocessed.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()
                raw_text = ocr_space_api(img_bytes, ocr_api_key)
                st.write("**Raw OCR Output:**")
                st.text(raw_text)

            with st.spinner("Cleaning text with AI..."):
                clean_text = correct_text_with_gpt(raw_text, openai_api_key)
                st.success("✅ Corrected Text:")
                st.write(clean_text)
