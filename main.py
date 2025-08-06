import streamlit as st
from PIL import Image
import easyocr
from gtts import gTTS
import numpy as np
import uuid
import os
import cv2
import subprocess
import imageio_ffmpeg  # ✅ fix for ffmpeg on Streamlit Cloud

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

                # Save uploaded image
                image.save(img_path)

                # Generate audio
                tts = gTTS(text=extracted_text, lang='en')
                tts.save(audio_path)

                # Get audio duration using ffprobe
                try:
                    result = subprocess.run(
                        [imageio_ffmpeg.get_ffmpeg_exe(), "-i", audio_path, "-hide_banner", "-loglevel", "error",
                         "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    duration = float(result.stdout.strip())
                except Exception as e:
                    duration = 10  # fallback
                    st.warning(f"Could not get duration, using 10s. Error: {e}")

                # Read image with OpenCV
                frame = np.array(image)
                height, width, _ = frame.shape

                # Create video with OpenCV
                temp_video = f"{uuid.uuid4().hex}.mp4"
                fps = 1
                out = cv2.VideoWriter(temp_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
                for _ in range(int(duration)):
                    out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                out.release()

                # Combine video and audio using imageio-ffmpeg
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                subprocess.call([
                    ffmpeg_path, '-y', '-i', temp_video, '-i', audio_path,
                    '-c:v', 'copy', '-c:a', 'aac', '-shortest', video_path
                ])

                st.success("✅ Video generated successfully!")
                st.video(video_path)

                # Clean up temp files
                os.remove(img_path)
                os.remove(audio_path)
                os.remove(temp_video)
