import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# Import modules
from modules.face_detection import detect_faces
from modules.face_blur import blur_faces
from modules.cartoonify import cartoonify
from modules.background_blur import blur_background
from modules.face_count import count_and_label_faces
from modules.filters import apply_grayscale, apply_sepia
from modules.eye_classification import classify_eyes

st.set_page_config(page_title="Visionary Face Processor", page_icon="👤", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #1e1e2e;
        color: #cdd6f4;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #313244;
        color: #cdd6f4;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45475a;
        color: #f5e0dc;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👤 Visionary Face Processor")
st.subheader("Advanced Computer Vision Image Processing")

# Sidebar
st.sidebar.title("🛠️ Controls")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert file to opencv image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    original_image = image.copy()

    st.sidebar.success("Image uploaded successfully!")

    # Options in sidebar
    st.sidebar.markdown("### 👥 Face Tools")
    feature = st.sidebar.selectbox("Choose a feature:", 
        ["Original", "Face Detection", "Face Blur", "Face Count", "Eye Classification", "Background Focus", "Cartoonify", "Grayscale", "Sepia Filter"])

    processed_image = original_image.copy()

    if feature == "Face Detection":
        processed_image = detect_faces(processed_image)
    elif feature == "Face Blur":
        processed_image = blur_faces(processed_image)
    elif feature == "Face Count":
        processed_image = count_and_label_faces(processed_image)
    elif feature == "Eye Classification":
        processed_image = classify_eyes(processed_image)
    elif feature == "Background Focus":
        processed_image = blur_background(processed_image)
    elif feature == "Cartoonify":
        processed_image = cartoonify(processed_image)
    elif feature == "Grayscale":
        processed_image = apply_grayscale(processed_image)
    elif feature == "Sepia Filter":
        processed_image = apply_sepia(processed_image)

    # Display images
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖼️ Original Image")
        st.image(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), use_container_width=True)
    
    with col2:
        st.markdown(f"### ✨ Result: {feature}")
        st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), use_container_width=True)

    # Download button
    result_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
    result_pil = Image.fromarray(result_rgb)
    
    # Save to buffer
    import io
    buf = io.BytesIO()
    result_pil.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    st.sidebar.markdown("### 💾 Export")
    st.sidebar.download_button(
        label="Download Result",
        data=byte_im,
        file_name="processed_image.jpg",
        mime="image/jpeg"
    )
else:
    st.info("Please upload an image to start processing.")
    
    # Show sample layout
    st.image("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
             caption="Example Face Image", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("Built with Python & OpenCV")
