import os
import cv2
import dlib
import numpy as np

def apply_lips_color(img, r, g, b):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initialize the face detector and shape predictor
    detector = dlib.get_frontal_face_detector()
    predictor_path = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")
    predictor = dlib.shape_predictor(predictor_path)

    # Detect faces in the grayscale image
    faces = detector(gray_img)
    if not faces:
        raise ValueError("No faces detected in the image.")

    # Initialize mask for lips
    lip_mask = np.zeros_like(img)

    # Process each detected face
    for face in faces:
        # Detect facial landmarks
        landmarks = predictor(gray_img, face)
        landmarks_points = []

        # Collect all 68 landmark points
        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmarks_points.append([x, y])

        # Convert landmarks to a NumPy array
        landmarks_points = np.array(landmarks_points)

        # Create a lip mask using the landmark indices for lips (48 to 67)
        cv2.fillPoly(lip_mask, [landmarks_points[48:68]], (255, 255, 255))

    # Create a mask with the selected lip color
    lip_img_color = np.zeros_like(lip_mask)
    lip_img_color[:] = (b, g, r)  # BGR format for OpenCV
    lip_img_color = cv2.bitwise_and(lip_mask, lip_img_color)

    # Apply Gaussian blur to soften the lip color effect
    lip_img_color = cv2.GaussianBlur(lip_img_color, (7, 7), 10)

    # Blend the original image with the colored lips
    final_makeup = cv2.addWeighted(img, 1, lip_img_color, 0.3, 0)

    return final_makeup