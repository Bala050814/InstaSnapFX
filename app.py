import os
import ctypes
import numpy as np
import cv2
import platform

# Get the absolute path to the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the correct library based on the operating system
if platform.system() == 'Windows':
    lib = ctypes.CDLL(os.path.join(current_dir, 'libgrayscale.dll'))  # Windows: .dll
else:
    lib = ctypes.CDLL(os.path.join(current_dir, 'libgrayscale.so'))  # Linux: .so

# Define function signature for the grayscale_vignette function from C code
lib.grayscale_vignette.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int]
lib.grayscale_vignette.restype = None

# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error opening camera.")
    exit()

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    flat = rgb_frame.flatten()
    c_array = (ctypes.c_uint8 * len(flat))(*flat)

    # Apply grayscale and vignette effect using the C function
    lib.grayscale_vignette(c_array, width, height)

    processed = np.ctypeslib.as_array(c_array).reshape((height, width, 3))
    bgr_output = cv2.cvtColor(processed, cv2.COLOR_RGB2BGR)

    # Display the resulting frame
    cv2.imshow("InstaSnapFX - Vignette Grayscale", bgr_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
