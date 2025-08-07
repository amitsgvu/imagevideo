import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import pytesseract

st.set_page_config(page_title="OCR App", layout="centered")
st.title("🧠 Clean OCR from Image")

def preprocess_image(image):
    # Convert to grayscale
    gray = image.convert("L")
    
    # Increase contrast
    contrast = ImageEnhance.Contrast(gray).enhance(2.0)
    
    # Increase sharpness
    sharp = ImageEnhance.Sharpness(contrast).enhance(2.0)
    
    # Resize (Tesseract works better on large images)
    resized = sharp.resize((sharp.width * 2, sharp.height * 2))
    
    # Apply autocontrast
    final = ImageOps.autocontrast(resized)
    
    return final

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        processed = preprocess_image(image)
        config = "--oem 3 --psm 6"
        text = pytesseract.image_to_string(processed, config=config)

        # Clean up
        clean_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])

        st.subheader("📋 Extracted Text")
        st.text(clean_text)
