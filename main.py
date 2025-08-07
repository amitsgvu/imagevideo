import streamlit as st
from PIL import Image
import easyocr
import tempfile
import os

st.title("🧠 Image to Text OCR App (EasyOCR)")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Save the image to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        image.save(temp_file.name)
        temp_image_path = temp_file.name

    st.write("🔍 Extracting text...")

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])  # You can add more languages if needed

    # Perform OCR
    results = reader.readtext(temp_image_path, detail=0)  # detail=0 returns just text

    # Show results
    extracted_text = "\n".join(results)
    st.text_area_
