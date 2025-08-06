import streamlit as st
import easyocr
from gtts import gTTS
from PIL import Image
import os
import cv2
import uuid
import subprocess

st.set_page_config(page_title="Image to Learning Video")

st.title("📚 Upload Image ➡ Get Learning Video")

uploaded_file = st.file_uploader("Upload an educational image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Reading text from image..."):
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(np.array(image), detail=0)
        extracted_text = " ".join(result).strip()

    if extracted_text:
        st.success("✅ Text successfully extracted.")
        st.text_area("📖 Extracted Text", extracted_text, height=100)

        with st.spinner("🔊 Generating audio..."):
            tts = gTTS(text=extracted_text)
            audio_path = f"temp_{uuid.uuid4().hex}.mp3"
            tts.save(audio_path)

        with st.spinner("🎞 Creating video..."):
            img_path = f"frame_{uuid.uuid4().hex}.jpg"
            image.save(img_path)

            video_path = f"video_{uuid.uuid4().hex}.mp4"

            # Use ffmpeg to generate video
            subprocess.call([
                'ffmpeg', '-y', '-loop', '1', '-i', img_path,
                '-i', audio_path,
                '-c:v', 'libx264', '-tune', 'stillimage',
                '-c:a', 'aac', '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-shortest', video_path
            ])

        st.video(video_path)

        # Cleanup temp files
        os.remove(audio_path)
        os.remove(img_path)
        # You can also optionally remove the video file
        # os.remove(video_path)
    else:
        st.warning("❌ No readable text found in the image.")
