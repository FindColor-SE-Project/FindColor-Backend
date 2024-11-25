import os
import cv2
import dlib
import numpy as np

def apply_blush_color(img, r, g, b):
    # Define the cheek color in BGR format (OpenCV uses BGR ordering)
    cheek_color = (b, g, r)

    # Convert the image to grayscale for face detection
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initialize face detector and facial landmark predictor
    detector = dlib.get_frontal_face_detector()

    # Use the absolute path for the predictor file
    predictor_path = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")
    predictor = dlib.shape_predictor(predictor_path)

    # Detect faces
    faces = detector(gray_img)
    if not faces:
        raise ValueError("No faces detected in the image.")

    # Process each detected face
    for face in faces:
        # Get the coordinates of the bounding box
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()

        # Detect facial landmarks
        landmarks = predictor(gray_img, face)

        # Define the indices for the left and right areas of the cheeks
        left_cheek_indices = [0, 1, 2, 3, 31, 30, 29, 28, 27, 39, 40, 41, 36]
        right_cheek_indices = [13, 14, 15, 16, 45, 46, 47, 42, 27, 28, 29, 35]

        # Extract landmark points for the left and right areas of the cheeks
        left_cheek_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in left_cheek_indices],
                                        dtype=np.int32)
        right_cheek_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in right_cheek_indices],
                                         dtype=np.int32)

        # Scale down the landmarks by 20%
        scale_factor = 0.6
        center_left = np.mean(left_cheek_landmarks, axis=0)
        center_right = np.mean(right_cheek_landmarks, axis=0)
        left_cheek_landmarks = ((left_cheek_landmarks - center_left) * scale_factor + center_left).astype(np.int32)
        right_cheek_landmarks = ((right_cheek_landmarks - center_right) * scale_factor + center_right).astype(np.int32)

        # Create masks for the left and right areas of the cheeks
        left_cheek_mask = np.zeros_like(img)
        right_cheek_mask = np.zeros_like(img)

        cv2.fillPoly(left_cheek_mask, [left_cheek_landmarks], (255, 255, 255))
        cv2.fillPoly(right_cheek_mask, [right_cheek_landmarks], (255, 255, 255))

        # Combine the cheek masks
        cheek_mask = cv2.bitwise_or(left_cheek_mask, right_cheek_mask)

        # Create a mask with the selected cheek color
        cheek_img_color = np.zeros_like(img)
        cheek_img_color[:] = cheek_color
        cheek_img_color = cv2.bitwise_and(cheek_mask, cheek_img_color)

        # Convert the cheek image to HSV and adjust saturation and brightness
        cheek_img_hsv = cv2.cvtColor(cheek_img_color, cv2.COLOR_BGR2HSV)
        saturation_factor = 1.5
        brightness_factor = 0.5

        cheek_img_hsv[:, :, 1] = np.clip(cheek_img_hsv[:, :, 1] * saturation_factor, 0, 255)
        cheek_img_hsv[:, :, 2] = np.clip(cheek_img_hsv[:, :, 2] * brightness_factor, 0, 255)

        cheek_img_color = cv2.cvtColor(cheek_img_hsv, cv2.COLOR_HSV2BGR)

        # Increase the GaussianBlur kernel size for a more noticeable effect
        cheek_img_color = cv2.GaussianBlur(cheek_img_color, (45, 45), 50)

        # Blend the cheek mask onto the original image with a stronger blending factor
        final_makeup_cheek = cv2.addWeighted(img, 1, cheek_img_color, 0.9, 0)

    return final_makeup_cheek
