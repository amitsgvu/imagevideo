import streamlit as st
from PIL import Image, ImageEnhance
import requests
import io

# OCR.Space API endpoint
OCR_SPACE_URL = "https://api.ocr.space/parse/image"

# Function to preprocess image (increase contrast)
def preprocess_image(image):
    image = image.convert("L")  # grayscale
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # increase contrast
    return image

# Function to call OCR.Space API
def ocr_space_api(image_bytes, api_key):
    payload = {
        'apikey': api_key,
        'language': 'eng',
        'isOverlayRequired': False,
    }
    files = {
        'file': ('image.png', image_bytes),
    }
    response = requests.post(OCR_SPACE_URL, data=payload, files=files)
    result = response.json()
    if result.get("IsErroredOnProcessing"):
        st.error("OCR processing error: " + result.get("ErrorMessage", ["Unknown error"])[0])
        return ""
    parsed_results = result.get("ParsedResults")
    if parsed_results:
        text = parsed_results[0].get("ParsedText", "")
        return text.strip()
    return ""

# Streamlit app
st.title("📚 OCR.Space Educational Text Extractor")

uploaded_file = st.file_uploader("Upload an image with educational text (numbers, ABCs, charts)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    preprocessed = preprocess_image(image)

    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.image(preprocessed, caption="Preprocessed Image (grayscale + contrast)", use_column_width=True)

    api_key = st.text_input("Enter your OCR.Space API Key", type="password")

    if st.button("Extract Text") and api_key:
        with st.spinner("Performing OCR..."):
            # Convert preprocessed image to bytes
            img_byte_arr = io.BytesIO()
            preprocessed.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()

            extracted_text = ocr_space_api(img_bytes, api_key)

            if extracted_text:
                st.success("✅ Extracted Text:")
                st.text(extracted_text)
            else:
                st.warning("No text extracted. Try a clearer image or different preprocessing.")
    elif not api_key:
        st.info("Please enter your OCR.Space API key to extract text.")
