import streamlit as st
import easyocr
from gtts import gTTS
from PIL import Image
import numpy as np
import uuid
import os
import imageio.v3 as iio
import cv2

st.set_page_config(page_title="Image to Learning Video")

st.title("📘 Upload Educational Image → Learn via Video")

uploaded_file = st.file_uploader("Upload an educational image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Reading text from image..."):
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(np.array(image), detail=0)
        extracted_text = " ".join(result).strip()

    if extracted_text:
        st.success("✅ Text extracted!")
        st.text_area("Extracted Text", extracted_text, height=100)

        with st.spinner("🔊 Generating audio..."):
            tts = gTTS(text=extracted_text)
            audio_path = f"{uuid.uuid4().hex}.mp3"
            tts.save(audio_path)

        with st.spinner("🎞 Generating video..."):
            img_array = np.array(image.convert("RGB"))
            height, width, _ = img_array.shape
            fps = 1  # one frame per second

            # Create a list of identical frames to match audio duration
            import mutagen
            from mutagen.mp3 import MP3
            audio = MP3(audio_path)
            duration = int(audio.info.length)

            frames = [img_array] * (duration * fps)

            video_path = f"{uuid.uuid4().hex}.mp4"
            iio.imwrite(uri=video_path, format="mp4",_
