import streamlit as st
from PIL import Image, ImageOps
import pytesseract

# --- CONFIG ---
CONFIG = r'--oem 3 --psm 6'  # Assume a single uniform block of text

def preprocess_image(image):
    # Convert to grayscale
    gray = image.convert("L")
    
    # Resize to improve OCR accuracy
    gray = gray.resize((gray.width * 2, gray.height * 2))
    
    # Apply binary thresholding
    gray = ImageOps.autocontrast(gray)
    
    return gray

def extract_text(image):
    preprocessed = preprocess_image(image)
    text = pytesseract.image_to_string(preprocessed, config=CONFIG)
    
    # Optional: Clean output
    lines = text.splitlines()
    cleaned_lines = [line for line in lines if line.strip()]
    return "\n".join(cleaned_lines)

# --- STREAMLIT UI ---
st.set_page_config(page_title="Image OCR", layout="centered")
st.title("📄 OCR Text Extractor")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        text = extract_text(image)
        st.subheader("📝 Extracted Text")
        st.text(text)
