import streamlit as st
from google.cloud import vision
from PIL import Image
import io
import os

# Load credentials securely from Streamlit secrets
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]

st.title("🔍 Google Vision OCR")

uploaded_file = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    content = img_byte_arr.getvalue()

    # Google Vision client
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    texts = response.text_annotations
    if texts:
        extracted_text = texts[0].description
        st.text_area("📋 Extracted Text", extracted_text, height=300)
    else:
        st.warning("No text detected.")
