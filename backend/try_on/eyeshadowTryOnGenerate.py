import os
import cv2
import dlib
import numpy as np


def apply_eyeshadow_color(img, r, g, b):
    height_offset = 15
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
    eyeshadow_mask = np.zeros_like(img)

    def create_eyeshadow_mask(indices, height_offset, exclude_indices):
        """
        Create an eyeshadow mask by adding height only on the upper side,
        while excluding the inner eye region.
        """
        # Extract landmarks as a NumPy array
        points = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in indices], dtype=np.int32)

        # Exclude inner eye region
        exclude_points = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in exclude_indices], dtype=np.int32)

        # Create a shifted version of the points (upward offset for the upper side)
        upper_line = points.copy()
        upper_line[:, 1] -= height_offset  # Move points upward (negative y-offset)

        # Combine the original and shifted lines to form a polygon
        polygon = np.vstack((points, upper_line[::-1]))  # Reverse for closed shape

        # Draw the polygon on the mask
        temp_mask = np.zeros_like(eyeshadow_mask)
        cv2.fillPoly(temp_mask, [polygon], (255, 255, 255))

        # Subtract the excluded region from the eyeshadow mask
        exclude_mask = np.zeros_like(eyeshadow_mask)
        cv2.fillPoly(exclude_mask, [exclude_points], (255, 255, 255))
        masked_temp = cv2.bitwise_and(temp_mask, cv2.bitwise_not(exclude_mask))

        # Merge this mask into the global eyeshadow_mask
        np.maximum(eyeshadow_mask, masked_temp, out=eyeshadow_mask)

    # Process each detected face
    for face in faces:
        landmarks = predictor(gray_img, face)

        # Create masks for both eyes, excluding the inner eye regions
        left_eye_indices = [36, 37, 38, 39, 40, 41]
        right_eye_indices = [42, 43, 44, 45, 46, 47]
        create_eyeshadow_mask([36, 37, 38, 39], height_offset, left_eye_indices)  # Left eye
        create_eyeshadow_mask([42, 43, 44, 45], height_offset, right_eye_indices)  # Right eye

        left_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in left_eye_indices],
                                      dtype=np.int32)
        right_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in right_eye_indices],
                                       dtype=np.int32)

        left_eye_mask = np.zeros_like(img)
        right_eye_mask = np.zeros_like(img)

        cv2.fillPoly(left_eye_mask, [left_eye_landmarks], (255, 255, 255))
        cv2.fillPoly(right_eye_mask, [right_eye_landmarks], (255, 255, 255))

        # Combine eye masks
        eye_mask = cv2.bitwise_or(left_eye_mask, right_eye_mask)

    # Create a mask with the selected eyeshadow color
    eyeshadow = np.zeros_like(img)
    eyeshadow[:] = (b, g, r)  # BGR format for OpenCV
    colored_mask = cv2.bitwise_and(eyeshadow, eyeshadow_mask)

    # Blur the mask for smoother blending
    blurred_mask = cv2.GaussianBlur(colored_mask, (15, 15), 10)

    eye_mask_gray = cv2.cvtColor(eye_mask, cv2.COLOR_BGR2GRAY)
    _, eye_mask_binary = cv2.threshold(eye_mask_gray, 1, 255, cv2.THRESH_BINARY)

    final_eye_mask = cv2.subtract(blurred_mask, eye_mask)

    # Blend the original image with the blurred eyeshadow mask
    final_image = cv2.addWeighted(img, 1, final_eye_mask, 0.5, 0)

    return final_image