import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from gtts import gTTS
import os
import uuid
import subprocess

# Set up Streamlit UI
st.set_page_config(page_title="AI-Based Learning App")
st.title("📚 AI-based Learning from Educational Images")
st.write("Upload an image (like counting, ABCs, etc.) and I’ll generate audio + video narration.")

uploaded_file = st.file_uploader("Upload an educational image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR
    st.write("🔍 Reading text from the image...")
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(np.array(image), detail=0)

    # Combine text
    full_text = " ".join(result).strip()
    st.write("🧾 Text detected:", full_text)

    if full_text:
        # Generate TTS audio
        audio_path = f"/tmp/{uuid.uuid4()}.mp3"
        tts = gTTS(text=full_text, lang='en')
        tts.save(audio_path)
        st.audio(audio_path)

        # Save uploaded image to disk
        image_path = f"/tmp/{uuid.uuid4()}.png"
        image.save(image_path)

        # Generate video using ffmpeg
        video_path = f"/tmp/{uuid.uuid4()}.mp4"
        st.write("🎬 Generating video...")

        try:
            subprocess.run([
                'ffmpeg', '-y',
                '-loop', '1', '-i', image_path,
                '-i', audio_path,
                '-c:v', 'libx264', '-tune', 'stillimage',
                '-c:a', 'aac', '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-shortest', video_path
            ], check=True)

            # Show video
            st.video(video_path)
            st.success("✅ Video generated successfully!")

        except Exception as e:
            st.error("⚠️ Failed to generate video.")
            st.exception(e)
    else:
        st.warning("⚠️ No readable text found in the image.")
