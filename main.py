import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import io

# Title
st.title("📷 OCR App - Number to Text Reader")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert PIL to numpy
    image_np = np.array(image)

    # Load OCR reader
    with st.spinner("Reading text from image..."):
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(image_np)

    # Display extracted text
    st.subheader("📝 Extracted Text:")
    extracted_text = "\n".join([res[1] for res in results])
    st.text_area("Result", extracted_text, height=300)
