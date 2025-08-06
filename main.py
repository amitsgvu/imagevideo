import streamlit as st
import easyocr
from gtts import gTTS
from PIL import Image
import numpy as np
import uuid
import os
import imageio.v3 as iio
from mutagen.mp3 import MP3

st.set_page_config(page_title="📘 Image to Learning Video")

st.title("📚 Upload Image → Get Learning Video")

uploaded_file = st.file_uploader("Upload an educational image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(np.array(image), detail=0)
        extracted_text = " ".join(result).strip()

    if extracted_text:
        st.success("✅ Text extracted!")
        st.text_area("📖 Extracted Text", extracted_text, height=100)

        # Generate audio
        audio_file = f"{uuid.uuid4().hex}.mp3"
        with st.spinner("🔊 Generating audio..."):
            tts = gTTS(text=extracted_text)
            tts.save(audio_file)

        # Get audio duration
        audio = MP3(audio_file)
        duration = int(audio.info.length)

        # Create video frames
        frame = np.array(image)
        frames = [frame] * duration  # Repeat frame to match duration

        video_file = f"{uuid.uuid4().hex}.mp4"
        with st.spinner("🎞 Generating video..."):
            iio.imwrite(
                uri=video_file,
                format="mp4",
                fps=1,
                codec="libx264",
                bitrate="800k",
                data=frames
            )

        st.video(video_file)

        # Cleanup (optional on local)
        os.remove(audio_file)
        os.remove(video_file)

    else:
        st.warning("⚠️ Could not extract any text from the image.")
