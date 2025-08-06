import streamlit as st
import easyocr
from gtts import gTTS
import os
import re
from PIL import Image
import numpy as np

# OCR and Cleaning
def extract_clean_text(image):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(np.array(image), detail=0)
    
    # Clean text
    def clean_text(text_list):
        cleaned = []
        for text in text_list:
            text = text.strip().lower()
            text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
            if len(text) >= 2 and re.search(r"[a-zA-Z0-9]", text):
                cleaned.append(text)
        return cleaned

    return sorted(set(clean_text(result)))

# Streamlit UI
st.title("📚 AI Educational Image Reader")
uploaded_file = st.file_uploader("Upload any educational image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Reading image..."):
        words = extract_clean_text(image)

    if words:
        final_text = ". ".join(words) + "."
        st.success("✅ Clean text extracted:")
        st.write(final_text)

        # Generate audio
        tts = gTTS(final_text)
        audio_path = "output.mp3"
        tts.save(audio_path)

        st.audio(audio_path)
    else:
        st.warning("No valid educational text found.")
