import streamlit as st
from PIL import Image
import pytesseract
import numpy as np
import cv2

st.set_page_config(page_title="Image to Text", layout="centered")
st.title("📄 OCR Image Text Extractor")

def preprocess_image(pil_image):
    # Convert to OpenCV format
    img = np.array(pil_image.convert('RGB'))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize to double the size (helps OCR accuracy)
    scale_percent = 200
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    gray = cv2.resize(gray, dim, interpolation=cv2.INTER_LINEAR)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return thresh

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        st.subheader("🧪 Extracting text...")
        processed_image = preprocess_image(image)

        # OCR configuration
        config = "--oem 3 --psm 6"
        text = pytesseract.image_to_string(processed_image, config=config)

        cleaned_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        st.subheader("📋 Extracted Text")
        st.text(cleaned_text)
