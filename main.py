import streamlit as st
import pytesseract
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="Image to Text OCR", layout="centered")
st.title("📄 Extract Text from Image using Tesseract + OpenCV")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

def preprocess_image(image: Image.Image):
    img = np.array(image.convert("RGB"))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    processed = preprocess_image(image)
    st.image(processed, caption="Preprocessed Image", channels="GRAY", use_column_width=True)

    st.markdown("### 🔍 Extracting text...")
    config = r'--oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(processed, config=config)

    st.text_area("📋 Extracted Text", extracted_text.strip(), height=300)

    if st.button("Copy to Clipboard"):
        st.write("Use Ctrl+C to copy text above.")
else:
    st.info("👆 Upload an image to begin.")
