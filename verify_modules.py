import cv2
import os
import sys

# Add the modules directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from face_detection import detect_faces
    from face_blur import blur_faces
    from cartoonify import cartoonify
    from background_blur import blur_background
    from face_count import count_and_label_faces
    from filters import apply_grayscale, apply_sepia
    print("[SUCCESS] Modules imported successfully")
except ImportError as e:
    print(f"[ERROR] Module import failed: {e}")
    exit(1)

# Load the sample image
image_path = os.path.join(os.path.dirname(__file__), 'images', 'input.jpg')
img = cv2.imread(image_path)

if img is None:
    print(f"[ERROR] Failed to load image from {image_path}")
    exit(1)
print("[SUCCESS] Sample image loaded successfully")

# Test Face Detection
try:
    det_img = detect_faces(img.copy())
    cv2.imwrite(os.path.join(os.path.dirname(__file__), 'output', 'test_detection.jpg'), det_img)
    print("[SUCCESS] Face detection successful")
except Exception as e:
    print(f"[ERROR] Face detection failed: {e}")

# Test Face Blur
try:
    blur_img = blur_faces(img.copy())
    cv2.imwrite(os.path.join(os.path.dirname(__file__), 'output', 'test_blur.jpg'), blur_img)
    print("[SUCCESS] Face blur successful")
except Exception as e:
    print(f"[ERROR] Face blur failed: {e}")

# Test Cartoonify
try:
    cart_img = cartoonify(img.copy())
    cv2.imwrite(os.path.join(os.path.dirname(__file__), 'output', 'test_cartoon.jpg'), cart_img)
    print("[SUCCESS] Cartoonify successful")
except Exception as e:
    print(f"[ERROR] Cartoonify failed: {e}")

# Test Background Blur
try:
    bg_blur_img = blur_background(img.copy())
    cv2.imwrite(os.path.join(os.path.dirname(__file__), 'output', 'test_bg_blur.jpg'), bg_blur_img)
    print("[SUCCESS] Background blur successful")
except Exception as e:
    print(f"[ERROR] Background blur failed: {e}")

# Test Face Counting
try:
    count_img = count_and_label_faces(img.copy())
    cv2.imwrite(os.path.join(os.path.dirname(__file__), 'output', 'test_face_count.jpg'), count_img)
    print("[SUCCESS] Face counting successful")
except Exception as e:
    print(f"[ERROR] Face counting failed: {e}")

# Test Grayscale
try:
    gray_img = apply_grayscale(img.copy())
    cv2.imwrite(os.path.join(os.path.dirname(__file__), 'output', 'test_grayscale.jpg'), gray_img)
    print("[SUCCESS] Grayscale successful")
except Exception as e:
    print(f"[ERROR] Grayscale failed: {e}")

# Test Sepia
try:
    sepia_img = apply_sepia(img.copy())
    cv2.imwrite(os.path.join(os.path.dirname(__file__), 'output', 'test_sepia.jpg'), sepia_img)
    print("[SUCCESS] Sepia successful")
except Exception as e:
    print(f"[ERROR] Sepia failed: {e}")

print("\nVerification complete. Check the 'output' folder for results.")
