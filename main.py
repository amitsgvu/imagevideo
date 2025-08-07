import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import pytesseract

st.set_page_config(page_title="Image OCR", layout="centered")
st.title("📄 Image to Text OCR")

def preprocess_image(image):
    # Convert to grayscale
    gray = image.convert("L")
    
    # Enhance contrast
    contrast = ImageEnhance.Contrast(gray).enhance(2.0)
    
    # Sharpen image
    sharp = ImageEnhance.Sharpness(contrast).enhance(2.0)
    
    # Resize to improve OCR accuracy
    resized = sharp.resize((sharp.width * 2, sharp.height * 2))
    
    # Auto-adjust contrast
    final = ImageOps.autocontrast(resized)
    
    return final

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text"):
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # OCR config for accuracy
        config = "--oem 3 --psm 6"
        extracted_text = pytesseract.image_to_string(processed_image, config=config)

        # Clean up output
        cleaned_text = "\n".join([line.strip() for line in extracted_text.splitlines() if line.strip()])

        st.subheader("📝 Extracted Text")
        st.text(cleaned_text)
