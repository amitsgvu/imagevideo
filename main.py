import streamlit as st
from PIL import Image
import easyocr
from gtts import gTTS
import cv2
import numpy as np
import uuid
import os
from pydub import AudioSegment

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

                # Save audio
                audio_path = f"{uuid.uuid4().hex}.mp3"
                tts = gTTS(text=extracted_text, lang='en')
                tts.save(audio_path)

                # Load audio and get duration
                audio = AudioSegment.from_file(audio_path)
                duration = audio.duration_seconds

                # Prepare image for video
                frame = np.array(image)
                height, width, _ = frame.shape
                video_path = f"{uuid.uuid4().hex}.mp4"

                # Create video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                fps = 1  # 1 frame per second
                out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

                # Repeat frame for each second of audio
                for _ in range(int(duration)):
                    out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                out.release()

                # Merge video and audio using moviepy only for final muxing
                from moviepy.editor import VideoFileClip, AudioFileClip
                final_video = VideoFileClip(video_path)
                final_video = final_video.set_audio(AudioFileClip(audio_path))
                final_output = f"final_{uuid.uuid4().hex}.mp4"
                final_video.write_videofile(final_output, codec='libx264')

                # Show result
                st.success("✅ Video generated successfully!")
                st.video(final_output)

                # Cleanup
                os.remove(audio_path)
                os.remove(video_path)
