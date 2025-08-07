import streamlit as st
from PIL import Image, ImageOps
import pytesseract

# --- CONFIG ---
CONFIG = r'--oem 3 --psm 6'  # Assume a single uniform block of text

def preprocess_image(image):
    # Convert to grayscale
    gray = image.convert("L")
    
    # Resize to improve OCR accuracy
    gray = gray.resize((gray.width * 2, gray.height * 2))
    
    # Apply binary thresholding
    gray = ImageOps.autocontrast(gray)
    
    return gray

def extract_text(image):
