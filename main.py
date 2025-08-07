import streamlit as st
from PIL import Image
import pytesseract

def extract_text_from_image(image):
    # Convert image to grayscale (optional for cleaner results)
    gray_image = image.convert("L")  # "L" mode = grayscale
    text = pytesseract.image_to_string(gray_image, config='--psm 6')
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
