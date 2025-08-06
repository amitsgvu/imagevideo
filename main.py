import streamlit as st
from PIL import Image
import easyocr
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import os
import uuid

st.set_page_config(page_title="Image to Learning Video", layout="centered")

st.title("📚 Image to Learning Video Generator")

uploaded_file = st.file_uploader("Upload an Image of a Chapter/Page", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Reading text from image..."):
        # OCR using EasyOCR
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image, detail=0)
        extracted_text = " ".join(result)

    if extracted_text.strip() == "":
        st.error("❌ No readable text found in the image.")
    else:
        st.subheader("📝 Extracted Text:")
        st.write(extracted_text)

        if st.button("🎬 Generate Learning Video"):
            with st.spinner("Generating video..."):
                # Generate audio using gTTS
                tts = gTTS(text=extracted_text, lang='en')
                audio_path = f"temp_{uuid.uuid4().hex}.mp3"
                tts.save(audio_path)

                # Save image
                image_path = f"temp_{uuid.uuid4().hex}.png"
                image.save(image_path)

                # Create video
                clip = ImageClip(image_path).set_duration(10)
                clip = clip.set_audio(AudioFileClip(audio_path))
                video_path = f"output_{uuid.uuid4().hex}.mp4"
                clip.write_videofile(video_path, fps=24)

                # Display video
                st.success("✅ Video generated successfully!")
                st.video(video_path)

                # Clean up
                os.remove(image_path)
                os.remove(audio_path)
