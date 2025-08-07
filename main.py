import streamlit as st
from PIL import Image
import pytesseract

# Tesseract config to get better accuracy
CUSTOM_CONFIG = r'--oem 3 --psm 6'  # Assume uniform block of text

st.set_page_config(page_title="OCR App", layout="centered")
st.title("📄 Extract Text from Image")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        # Convert to grayscale
        gray = image.convert("L")

        # Run OCR with good config
        extracted_text = pytesseract.image_to_string(gray, config=CUSTOM_CONFIG)

        # Clean up result: remove empty lines & noise
        cleaned_text = "\n".join([
            line for line in extracted_text.splitlines()
            if line.strip() and not line.strip().isdigit()
        ])

        st.subheader("📝 Extracted Text")
        st.text(cleaned_text)
