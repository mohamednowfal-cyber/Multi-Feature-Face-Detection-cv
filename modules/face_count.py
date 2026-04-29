import cv2

def count_and_label_faces(image):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    count = 0

    for (x, y, w, h) in faces:
        count += 1

        # Draw rectangle
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Label each face
        cv2.putText(image, f"Face {count}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display total count
    cv2.putText(image, f"Total Faces: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    return image
