import base64
import io

import cv2
import numpy as np
from PIL import Image, ImageDraw

def crop_head(image_data, crop_width=400, crop_height=500, factor=1.2):
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

        # กำหนดขนาดครอปตายตัว
        x_new = max(0, center_x - crop_width // 2)
        y_new = max(0, center_y - crop_height // 2)

        # ตรวจสอบให้แน่ใจว่าภาพที่ตัดไม่เกินขอบเขต
        x_new = min(x_new, cv_image.shape[1] - crop_width)
        y_new = min(y_new, cv_image.shape[0] - crop_height)

        # Crop the head region with fixed size
        cropped_head = cv_image[y_new:y_new + crop_height, x_new:x_new + crop_width]
        cropped_head_pil = Image.fromarray(cv2.cvtColor(cropped_head, cv2.COLOR_BGR2RGB))

        # Resize cropped_head_pil to ensure it fits in the oval image
        cropped_head_pil = cropped_head_pil.resize((crop_width, crop_height), Image.LANCZOS)

        # Create oval mask
        mask = Image.new('L', (crop_width, crop_height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, crop_width, crop_height), fill=255)

        # Create an oval image with transparency
        oval_image = Image.new('RGBA', (crop_width, crop_height))

        # Paste the cropped head onto the oval image with the mask
        oval_image.paste(cropped_head_pil, (0, 0), mask)

        # Convert image to Base64
        buffered = io.BytesIO()
        oval_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_str

    return None
