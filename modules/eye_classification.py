import cv2

def classify_eyes(image):
    # Load classifiers
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml'
    )

    # Convert to grayscale and equalize histogram
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Detect faces with robust parameters
    faces = face_cascade.detectMultiScale(gray, 1.1, 7, minSize=(50, 50))

    for (x, y, w, h) in faces:
        # Add padding to ROI for better eye context
        pad_x, pad_y = int(w * 0.05), int(h * 0.05)
        y1, y2 = max(0, y - pad_y), min(image.shape[0], y + h + pad_y)
        x1, x2 = max(0, x - pad_x), min(image.shape[1], x + w + pad_x)
        
        roi_gray = gray[y1:y2, x1:x2]
        roi_color = image[y1:y2, x1:x2]

        # Detect eyes inside the face region with high minNeighbors for precision
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 15, minSize=(10, 10))

        # Classification logic based on number of eyes detected
        if len(eyes) >= 2:
            label = "Eyes Visible"
            color = (0, 255, 0) # Green
        else:
            label = "Eyes Not Visible"
            color = (0, 0, 255) # Red

        # Draw face rectangle
        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)

        # Label text above the face
        cv2.putText(image, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Draw rectangles around eyes (optional, but helpful for visual confirmation)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 1)

    return image
