import cv2
import numpy as np

# Grayscale filter
def apply_grayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Convert back to 3-channel BGR so it's compatible with other filters
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

# Sepia filter
def apply_sepia(image):
    # Sepia transition matrix
    kernel = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ])

    # Applying the transformation
    sepia_img = cv2.transform(image, kernel)
    
    # Clip values to [0, 255] and convert to uint8
    sepia_img = cv2.convertScaleAbs(sepia_img)

    return sepia_img
