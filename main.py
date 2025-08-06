import streamlit as st
from PIL import Image
import easyocr
from gtts import gTTS
import numpy as np
import os
import uuid
import subprocess
from mutagen.mp3 import MP3

st.title("🖼️ Image to Narrated Video (Streamlit-Compatible)")
st.write("Upload an educational image and generate a video with spoken text.")

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_id = str(uuid.uuid4())
    image_path = f"{image_id}.png"
    image.save(image_path)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(np.array(image), detail=0)
        extracted_text = " ".join(result)

    st.success("✅ Extracted Text:")
    st.write(extracted_text)

    if extracted_text.strip():
        with st.spinner("🔊 Generating audio..."):
            audio_path = f"{image_id}.mp3"
            tts = gTTS(text=extracted_text, lang="en")
            tts.save(audio_path)

        st.audio(audio_path)

        # Get audio duration
        audio = MP3(audio_path)
        duration = int(audio.info.length)

        with st.spinner("🎬 Generating video..."):
            video_path = f"{image_id}.mp4"
            subprocess.call([
                "ffmpeg", "-y",
                "-loop", "1", "-i", image_path,
                "-i", audio_path,
                "-c:v", "libx264", "-t", str(duration),
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-shortest", video_path
            ])

        st.success("✅ Video generated!")
        with open(video_path, "rb") as f:
            st.download_button("⬇️ Download Video", f, file_name="educational_video.mp4", mime="video/mp4")

        # Cleanup temp files
        os.remove(image_path)
        os.remove(audio_path)
        os.remove(video_path)

    else:
        st.error("❌ Could not detect text in image.")
