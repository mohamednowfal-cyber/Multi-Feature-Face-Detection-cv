import cv2

def cartoonify(image):
    # 1. Edge Mask
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, 
                                  cv2.ADAPTIVE_THRESH_MEAN_C, 
                                  cv2.THRESH_BINARY, 9, 9)

    # 2. Color Surface Processing
    # bilateralFilter reduces noise while keeping edges sharp
    color = cv2.bilateralFilter(image, 9, 300, 300)

    # 3. Combine Color with Edge Mask
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon
