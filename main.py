import streamlit as st
import requests

def ocr_space_file(file, api_key, language='eng'):
    url_api = 'https://api.ocr.space/parse/image'
    with open(file, 'rb') as f:
        response = requests.post(
            url_api,
            files={'filename': f},
            data={
                'apikey': api_key,
                'language': language,
                'OCREngine': 2
            },
        )
    result = response.json()
    return result.get("ParsedResults", [{}])[0].get("ParsedText", "No text found.")

st.title("🧠 OCR with OCR.Space API")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.read())

    api_key = st.secrets["OCR_SPACE_API_KEY"]

    with st.spinner("Extracting text..."):
        extracted_text = ocr_space_file("temp_image.png", api_key)
        st.success("Text extracted!")

    st.text_area("📋 Extracted Text", extracted_text, height=300)
