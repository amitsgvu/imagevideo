import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import tempfile

def extract_text_from_image(image):
    # Convert PIL to OpenCV
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    text = pytesseract.image_to_string(thresh, config='--oem 3 --psm 6')
    return text

st.title("🧠 OCR App")

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        result = extract_text_from_image(image)
        st.subheader("Extracted Text:")
        st.text(result)
