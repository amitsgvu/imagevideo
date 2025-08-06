import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from gtts import gTTS
import os
import uuid

# Set up Streamlit UI
st.set_page_config(page_title="AI-Based Learning App")
st.title("📚 AI-based Learning from Educational Images")
st.write("Upload an image (e.g., counting or ABCs) to generate audio narration.")

uploaded_file = st.file_uploader("Upload an educational image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR
    st.write("🔍 Reading text from the image...")
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(np.array(image), detail=0)

    full_text = " ".join(result).strip()
    st.write("🧾 Text detected:", full_text)

    if full_text:
        # Generate audio
        audio_path = f"/tmp/{uuid.uuid4()}.mp3"
        tts = gTTS(text=full_text, lang='en')
        tts.save(audio_path)
        st.audio(audio_path, format="audio/mp3")
        st.success("✅ Audio generated. You can use video editors (like Canva or Kapwing) to combine it with the image.")
    else:
        st.warning("⚠️ No text was detected in the image.")
