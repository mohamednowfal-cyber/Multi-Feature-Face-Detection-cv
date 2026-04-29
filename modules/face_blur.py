import cv2

def blur_faces(image):
    # Load the pre-trained Haar Cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # Apply blur to each detected face
    for (x, y, w, h) in faces:
        # Extract the ROI (Region of Interest)
        face_roi = image[y:y+h, x:x+w]
        
        # Apply Gaussian Blur
        # Kernel size (99, 99) makes it quite blurry; sigma 30 controls the spread
        blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
        
        # Put the blurred face back into the original image
        image[y:y+h, x:x+w] = blurred_face

    return image
