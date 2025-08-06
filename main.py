import streamlit as st
import easyocr
from PIL import Image
from gtts import gTTS
import tempfile
import os
import moviepy.editor as mpe
import base64

# Title
st.title("📚 Image to Educational Video")
st.write("Upload an educational image (e.g., textbook page, diagram, numbers) to generate a narrated video.")

# Upload
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR
    with st.spinner("🔍 Extracting text..."):
        reader = easyocr.Reader(['en'])  # Add more languages if needed
        result = reader.readtext(uploaded_file, detail=0)
        raw_text = " ".join(result)

    # Clean text
    def clean_text(text):
        text = text.replace("\n", " ")
        text = text.replace("o", "0")  # common OCR mistake
        text = text.replace("O", "0")
        text = text.replace("1 0", "10")
        text = text.strip()
        return text

    cleaned_text = clean_text(raw_text)

    st.subheader("📖 Extracted Text")
    st.write(cleaned_text)

    # Convert text to audio
    with st.spinner("🎤 Generating audio..."):
        tts = gTTS(cleaned_text)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)

    # Create video from image + audio
    with st.spinner("🎬 Creating video..."):
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(temp_img.name)

        image_clip = mpe.ImageClip(temp_img.name).set_duration(10)  # default 10s
        audio_clip = mpe.AudioFileClip(temp_audio.name)
        image_clip = image_clip.set_audio(audio_clip)
        video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        image_clip.write_videofile(video_path, fps=24)

    # Show video
    st.success("✅ Video generated!")
    with open(video_path, "rb") as f:
        video_bytes = f.read()
        st.video(video_bytes)

    # Download
    b64 = base64.b64encode(video_bytes).decode()
    href = f'<a href="data:video/mp4;base64,{b64}" download="educational_video.mp4">📥 Download Video</a>'
    st.markdown(href, unsafe_allow_html=True)
