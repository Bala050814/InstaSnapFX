import streamlit as st
import cv2
import numpy as np
import ctypes
from PIL import Image
import time

# Load the compiled C library
lib = ctypes.CDLL('./libgrayscale.dll')
lib.grayscale_vignette.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int]
lib.grayscale_vignette.restype = None

# Streamlit UI
st.set_page_config(layout="centered")
st.title("🎥 InstaSnapFX - Vignette Grayscale Filter")

# UI Controls
run = st.toggle("Start Webcam")
mirror = st.checkbox("🪞 Mirror Video (Selfie View)", value=True)

# Frame placeholder
frame_placeholder = st.empty()

# Main loop
if run:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("❌ Unable to access the webcam.")
    else:
        st.success("✅ Webcam is running...")

    while run and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Failed to capture frame.")
            break

        # Flip if mirroring is enabled
        if mirror:
            frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        flat = rgb.flatten()
        c_array = (ctypes.c_uint8 * len(flat))(*flat)

        # Apply grayscale + vignette effect using the C DLL
        lib.grayscale_vignette(c_array, width, height)

        # Convert back to image
        processed = np.ctypeslib.as_array(c_array).reshape((height, width, 3))
        img = Image.fromarray(processed)
        frame_placeholder.image(img)

        # Slight delay to reduce CPU usage
        time.sleep(0.03)

    cap.release()
    st.info("🛑 Webcam stopped.")
else:
    st.info("Toggle the switch above to start the webcam.")
