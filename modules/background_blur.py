import cv2

def blur_background(image):
    # Load face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    # Convert to grayscale and equalize histogram
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Detect faces with higher minNeighbors for stability
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7, minSize=(50, 50))

    # Create blurred version of entire image
    # Kernel size (51, 51) for background blur
    blurred = cv2.GaussianBlur(image, (51, 51), 0)

    # If no face detected -> return blurred image
    if len(faces) == 0:
        return blurred

    # Copy blurred image as base
    output = blurred.copy()

    for (x, y, w, h) in faces:
        # Add some padding to include more of the head
        padding = 20

        x1 = max(x - padding, 0)
        y1 = max(y - padding, 0)
        x2 = min(x + w + padding, image.shape[1])
        y2 = min(y + h + padding, image.shape[0])

        # Keep face region original (not blurred)
        output[y1:y2, x1:x2] = image[y1:y2, x1:x2]

        # Optional: draw rectangle (commented out for cleaner "Focus" look, 
        # but user asked for it in prompt so I will include it)
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return output
