import streamlit as st
from PIL import Image
import easyocr
from gtts import gTTS
import cv2
import numpy as np
import uuid
import os
from moviepy.editor import VideoFileClip, AudioFileClip

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

                # Save audio using gTTS
                audio_path = f"{uuid.uuid4().hex}.mp3"
                tts = gTTS(text=extracted_text, lang='en')
                tts.save(audio_path)

                # Save image and prepare frame
                frame = np.array(image)
                height, width, _ = frame.shape
                video_path = f"{uuid.uuid4().hex}.mp4"

                # Create a video of 10 seconds, 1 frame per second
                fps = 1
                duration = 10
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
                for _ in range(duration):
                    out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                out.release()

                # Combine image video with audio
                final_output = f"final_{uuid.uuid4().hex}.mp4"
                videoclip = VideoFileClip(video_path)
                audioclip = AudioFileClip(audio_path)
                videoclip = videoclip.set_audio(audioclip)
                videoclip.write_videofile(final_output, codec='libx264')

                # Display
                st.success("✅ Video generated successfully!")
                st.video(final_output)

                # Clean up
                os.remove(audio_path)
                os.remove(video_path)
