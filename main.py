import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import io
import re
from openocr import OpenOCR  # Python interface for the OpenOCR toolkit
from gtts import gTTS

# Initialize OpenOCR once
ocr = OpenOCR(device="cpu")  # uses SVTRv2, ONNX backend via CPU

def preprocess(image: Image.Image) -> np.ndarray:
    img = image.convert("L")
    img = img.filter(ImageFilter.MedianFilter(3))
    img = img.resize((img.width * 2, img.height * 2))
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.5)
    return np.array(img)

def clean_text(lines):
    texts = []
    for ln in lines:
        line = ln.strip().lower()
        line = re.sub(r"[^a-z0-9\s]", "", line)
        if 2 <= len(line) <= 20:
            texts.append(line)
    return sorted(set(texts))

st.title("📚 High‑Accuracy Educational OCR with OpenOCR (SVTRv2)")
uploaded = st.file_uploader("Upload educational image (e.g. charts, ABCs, handwritten)", type=["png","jpg","jpeg"])
if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded image", use_column_width=True)
    arr = preprocess(img)
    with st.spinner("🔍 Extracting text..."):
        lines = ocr.recognize(arr)  # returns list of text lines
    cleaned = clean_text(lines)
    if cleaned:
        out = ". ".join(cleaned).capitalize() + "."
        st.success("✅ Cleaned extracted text:")
        st.write(out)
        tts = gTTS(out)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        st.audio(buf.read(), format="audio/mp3")
    else:
        st.warning("❌ No readable educational text found.")
