import streamlit as st
import cv2
import numpy as np
import ctypes
from PIL import Image
import tempfile
import time

st.set_page_config(page_title="InstaSnapFX", layout="centered")
st.title("📷 InstaSnapFX - Webcam Grayscale + Vignette Filter")

# Load the compiled C library
try:
    lib = ctypes.CDLL('./libgrayscale.so')
    lib.grayscale_vignette.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int]
    lib.grayscale_vignette.restype = None
except Exception as e:
    st.error("⚠️ Unable to load C library: libgrayscale.so")
    st.stop()

run = st.toggle("▶️ Start Webcam")
mirror = st.checkbox("🔁 Mirror (selfie view)", value=True)

frame_placeholder = st.empty()

if run:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("❌ Unable to access webcam.")
        st.stop()

    st.success("📸 Webcam running...")

    while run and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Unable to read frame.")
            break

        if mirror:
            frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        flat = rgb.flatten()
        c_array = (ctypes.c_uint8 * len(flat))(*flat)

        # Apply C filter
        lib.grayscale_vignette(c_array, width, height)

        output = np.ctypeslib.as_array(c_array).reshape((height, width, 3))
        img = Image.fromarray(output)
        frame_placeholder.image(img)

        time.sleep(0.03)

    cap.release()
    st.info("🛑 Webcam stopped.")
else:
    st.info("Toggle the switch to start your webcam.")
