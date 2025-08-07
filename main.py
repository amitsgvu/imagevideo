import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

# Config for tesseract to treat image as a block of text
TESSERACT_CONFIG = r'--oem 3 --psm 6'

def preprocess_image(image: Image.Image) -> Image.Image:
    # Convert to grayscale
    gray = image.convert("L")
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(gray)
    sharp = enhancer.enhance(2.0)
    
    # Auto contrast
    auto_contrast = ImageOps.autocontrast(sharp)
    
    # Resize (important for better OCR results)
    large = auto_contrast.resize((auto_contrast.width * 2, auto_contrast.height * 2))
    
    return large

def extract_text(image: Image.Image) -> str:
    processed = preprocess_image(image)
    raw_text = pytesseract.image_to_string(processed, config=TESSERACT_CONFIG)

    # Clean extra whitespace and blank lines
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    return "\n".join(lines)

# Streamlit UI
st.set_page_config(page_title="📄 Image OCR App", layout="centered")
st.title("🧠 OCR: Extract Text from Image")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        result = extract_text(image)
        st.subheader("📋 Extracted Text")
        st.text(result)
