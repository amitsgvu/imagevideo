import streamlit as st
from PIL import Image
import easyocr
from gtts import gTTS
import numpy as np
import uuid
import os
import cv2
import subprocess
import imageio_ffmpeg

st.set_page_config(page_title="Image to Learning Video", layout="centered")

st.title("📚 Image to Learning Video Generator")

uploaded_file = st.file_uploader("Upload an Image of a Chapter/Page", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Reading text from image..."):
        reader = easyocr.Reader(['en'])
        result = reader.readtext(np.array(image), detail=0)
        extracted_text = " ".join(result)

    if extracted_text.strip() == "":
        st.error("❌ No readable text found in the image.")
    else:
        st.subheader("📝 Extracted Text:")
        st.write(extracted_text)

        if st.button("🎬 Generate Learning Video"):
            with st.spinner("Generating video..."):

                img_path = f"{uuid.uuid4().hex}.jpg"
                audio_path = f"{uuid.uuid4().hex}.mp3"
                video_path = f"{uuid.uuid4().hex}_output.mp4"
                temp_video = f"{uuid.uuid4().hex}.mp4"

                # Save image
                image.save(img_path)

                # Generate audio
                tts = gTTS(text=extracted_text, lang='en')
                tts.save(audio_path)

                # Set default duration (10 seconds)
                duration = 10
                frame = np.array(image)
                height, width, _ = frame.shape
                fps = 1

                out = cv2.VideoWriter(temp_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
                for _ in range(duration):
                    out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                out.release()

                # Combine audio and image video
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                subprocess.call([
                    ffmpeg_path, '-y', '-i', temp_video, '-i', audio_path,
                    '-c:v', 'copy', '-c:a', 'aac', '-shortest', video_path
                ])

                st.success("✅ Video generated!")
                st.video(video_path)

                # Cleanup
                os.remove(img_path)
                os.remove(audio_path)
                os.remove(temp_video)
