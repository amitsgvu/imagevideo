import streamlit as st
from google.cloud import vision
import json
import os

# Load credentials from Streamlit secrets
service_account_info = json.loads(st.secrets["GOOGLE_APPLICATION_CREDENTIALS_JSON"])

# Authenticate client
client = vision.ImageAnnotatorClient.from_service_account_info(service_account_info)

st.title("📄 Image to Text OCR using Google Vision API")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    st.image(image_bytes, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        image = vision.Image(content=image_bytes)
        response = client.text_detection(image=image)
        texts = response.text_annotations

    if texts:
        st.subheader("📝 Extracted Text:")
        st.text_area("Detected Text", texts[0].description.strip(), height=200)
    else:
        st.warning("No text detected.")
