import os
import cv2
import dlib
import numpy as np


def apply_eyeshadow_color(img, r, g, b, height_offset=15):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initialize face detector and shape predictor
    detector = dlib.get_frontal_face_detector()
    predictor_path = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")
    predictor = dlib.shape_predictor(predictor_path)

    # Detect faces in the image
    faces = detector(gray_img)
    if not faces:
        raise ValueError("No faces detected in the image.")

    # Initialize mask for eyeshadow
    eye_mask = np.zeros_like(img)

    def create_eyeshadow_mask(indices, height_offset):
        """
        Create an eyeshadow mask by adding height only on the upper side.
        """
        # Extract landmarks as a NumPy array
        points = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in indices], dtype=np.int32)

        # Create a shifted version of the points (upward offset for the upper side)
        upper_line = points.copy()
        upper_line[:, 1] -= height_offset  # Move points upward (negative y-offset)

        # Combine the original and shifted lines to form a polygon
        polygon = np.vstack((points, upper_line[::-1]))  # Reverse for closed shape

        # Draw the polygon on the mask
        cv2.fillPoly(eye_mask, [polygon], (255, 255, 255))

    # Process each detected face
    for face in faces:
        landmarks = predictor(gray_img, face)

        # Create masks for both eyes, adding height only to the upper side
        create_eyeshadow_mask([36, 37, 38, 39], height_offset)  # Left eye
        create_eyeshadow_mask([42, 43, 44, 45], height_offset)  # Right eye

    # Create a mask with the selected eyeshadow color
    eyeshadow = np.zeros_like(img)
    eyeshadow[:] = (b, g, r)  # BGR format for OpenCV
    colored_mask = cv2.bitwise_and(eyeshadow, eye_mask)

    # Blur the mask for smoother blending
    blurred_mask = cv2.GaussianBlur(colored_mask, (15, 15), 10)

    # Blend the original image with the blurred eyeshadow mask
    final_image = cv2.addWeighted(img, 1, blurred_mask, 0.5, 0)

    return final_image
