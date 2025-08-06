import os
import streamlit as st
from google.cloud import vision

# Optional: Set path to credentials if you want to specify directly in code
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"

def detect_text(image_bytes):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    else:
        return "No text detected."

st.title("Google Cloud Vision OCR with Streamlit")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    st.image(image_bytes, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Extracting text..."):
        text = detect_text(image_bytes)

    st.subheader("Extracted Text:")
    st.text_area("", text, height=200)
