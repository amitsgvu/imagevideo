import streamlit as st
from PIL import Image
import easyocr
from gtts import gTTS
import numpy as np
import imageio.v3 as iio
from mutagen.mp3 import MP3
import os
import uuid

st.title("📚 Image to Learning Video (For Kids)")
st.write("Upload an educational image to generate a narrated video.")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Save uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    image_id = str(uuid.uuid4())
    image_path = f"{image_id}.png"
    image.save(image_path)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Reading text from image..."):
        reader = easyocr.Reader(['en'])
        result = reader.readtext(np.array(image), detail=0)
        extracted_text = " ".join(result)

    st.success("✅ Text extracted:")
    st.write(extracted_text)

    if extracted_text.strip():
        with st.spinner("🔊 Converting to speech..."):
            tts = gTTS(text=extracted_text, lang="en")
            audio_path = f"{image_id}.mp3"
            tts.save(audio_path)

        st.audio(audio_path)

        # Get duration of audio
        audio = MP3(audio_path)
        duration = int(audio.info.length)

        # Repeat image as frames
        with st.spinner("🎞️ Creating video..."):
            video_path = f"{image_id}.mp4"
            frame = np.array(image)
            frames = [frame] * duration

            with iio.imopen(video_path, "w", plugin="pyav") as writer:
                for frame in frames:
                    writer.write(frame)

        st.success("✅ Video generated!")

        with open(video_path, "rb") as f:
            st.download_button("⬇️ Download Video", f, file_name="learning_video.mp4", mime="video/mp4")

        # Cleanup
        os.remove(image_path)
        os.remove(audio_path)
        os.remove(video_path)
    else:
        st.error("❌ No text found in the image.")
