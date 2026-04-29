import cv2

def classify_eyes(image):
    # Load classifiers
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml'
    )

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]

        # Detect eyes inside the face region
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4)

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
