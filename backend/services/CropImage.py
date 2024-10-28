import base64
import io

import cv2
import numpy as np
from PIL import Image, ImageDraw
import os

def detect_and_crop_head(image_data, factor=1.2):  # ลด factor
    # Load the pre-trained face detection model from OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert image data from bytes to PIL format
    image = Image.open(image_data)

    # Convert PIL image to OpenCV format (BGR)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        center_x = x + w // 2
        center_y = y + h // 2
        size = int(max(w, h) * factor)
        x_new = max(0, center_x - size // 2)
        y_new = max(0, center_y - size // 2)

        # Crop the head region
        cropped_head = cv_image[y_new:y_new + size, x_new:x_new + size]
        cropped_head_pil = Image.fromarray(cv2.cvtColor(cropped_head, cv2.COLOR_BGR2RGB))

        # Resize and create oval mask
        cropped_head_pil = cropped_head_pil.resize((400, 500), Image.LANCZOS)
        mask = Image.new('L', (400, 500), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 400, 500), fill=255)
        oval_image = Image.new('RGBA', (400, 500))
        oval_image.paste(cropped_head_pil, (0, 0), mask)

        # Convert image to Base64
        buffered = io.BytesIO()
        oval_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_str

    return None
