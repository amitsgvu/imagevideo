import streamlit as st
from PIL import Image
import easyocr
import tempfile
import os

st.title("🧠 Image to Text OCR App (EasyOCR)")

uploaded_file = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='🖼️ Uploaded Image', use_column_width=True)

    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        image.save(temp_file.name)
        temp_image_path = temp_file.name

    st.write("🔍 Extracting text from image...")

    # OCR using EasyOCR
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(temp_image_path, detail=0)  # detail=0 gives just text

    # Show extracted text
    extracted_text = "\n".join(results)
    st.text_area("📋 Extracted Text", extracted_text, height=300)

    # Clean up
    os.remove(temp_image_path)
