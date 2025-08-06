import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
from gtts import gTTS
import io
import cv2
import re
from paddleocr import PaddleOCR

# Initialize PaddleOCR once (global)
ocr_model = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

# Image preprocessing using OpenCV + Pillow
def preprocess_image(image):
    image = image.convert("RGB")
    image = image.resize((image.width * 2, image.height * 2))  # upscale for clarity
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.5)  # strong contrast

    # Convert to OpenCV format
    open_cv_image = np.array(image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # Denoise
    gray = cv2.fastNlMeansDenoising(gray, h=30)

    # Thresholding for binarization
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

# Clean OCR output
def clean_text(results):
    text_list = []
    for result in results:
        line = result[1][0].strip().lower()
        line = re.sub(r"[^a-zA-Z0-9\s]", "", line)
        if 2 <= len(line) <= 20:
            text_list.append(line)
    return sorted(set(text_list))

# Extract text using PaddleOCR
def extract_text(image_array):
    results = ocr_model.ocr(image_array, cls=True)
    flat_results = [item for sublist in results for item in sublist]
    return clean_text(flat_results)

# Streamlit UI
st.title("📚 AI Educational Image Reader (High Accuracy)")
uploaded_file = st.file_uploader("Upload an educational image (e.g., numbers, ABCs, charts)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    preprocessed_array = preprocess_image(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Reading and cleaning text..."):
        clean_results = extract_text(preprocessed_array)

    if clean_results:
        final_text = ". ".join(clean_results).capitalize() + "."
        st.success("✅ Clean text extracted:")
        st.write(final_text)

        # Text-to-speech
        tts = gTTS(final_text)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp.read(), format="audio/mp3")
    else:
        st.warning("❌ No readable educational text found.")
