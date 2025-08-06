from PIL import Image, ImageEnhance, ImageFilter
import io

# Helper: preprocess image
def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("L")  # Convert to grayscale
    image = image.filter(ImageFilter.MedianFilter())          # Denoise
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Increase contrast
    return image

# Use in your code
if uploaded_file:
    image_bytes = uploaded_file.read()
    processed_image = preprocess_image(image_bytes)

    buf = io.BytesIO()
    processed_image.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    st.image(image_bytes, caption="Preprocessed Image", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        image = vision.Image(content=image_bytes)
        response = client.text_detection(image=image)
        texts = response.text_annotations
