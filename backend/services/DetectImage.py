import cv2
import numpy as np
from PIL import Image

def detect_image(image_data):  # ลด factor
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert image data from bytes to PIL format
    image = Image.open(image_data)

    # Convert PIL image to OpenCV format (BGR)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    return len(faces) > 0
