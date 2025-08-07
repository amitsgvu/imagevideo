import streamlit as st
from PIL import Image
import pytesseract

# Optional: Only if you're running locally and tesseract isn't on PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image):
    # Convert to grayscale to improve OCR
    gray = image.convert("L")
    
    # Use proper OCR configuration
    config = "--oem 3 --psm 6"  # Assume a single block of text
    text = pytesseract.image_to_string(gray, config=config)
    return text

st.title("📄 OCR App: Clean Text from Image")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        extracted_text = extract_text(image)
        st.subheader("📝 Extracted Text:")
        st.text(extracted_text)
