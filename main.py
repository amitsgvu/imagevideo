import streamlit as st
from google.cloud import vision
from PIL import Image, ImageEnhance, ImageFilter
import io
import os

# Load credentials from environment (assumes set already)
client = vision.ImageAnnotatorClient()

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    image = image.filter(ImageFilter.MedianFilter())  # Denoise
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Boost contrast
    return image

st.title("📷 Image to Text - Google Vision OCR")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image_bytes = uploaded_file.read()
    processed_image = preprocess_image(image_bytes)

    # Convert PIL image back to bytes
    buf = io.BytesIO()
    processed_image.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    st.image(image_bytes, caption="🖼️ Processed Image", use_column_width=True)

    image = vision.Image(content=image_bytes)
    image_context = vision.ImageContext(language_hints=["en"])
    response = client.text_detection(image=image, image_context=image_context)

    texts = response.text_annotations

    if texts:
        st.subheader("📝 Extracted Text")
        st.text_area("Detected Text", texts[0].description.strip(), height=250)

        st.subheader("🔍 OCR Debug (each block)")
        for i, text in enumerate(texts[1:], 1):
            st.write(f"{i}. {text.description}")
    else:
        st.warning("⚠️ No text detected. Try a clearer image.")
