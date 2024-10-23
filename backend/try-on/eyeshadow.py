import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt

# Load the image
img = cv2.imread('pic4.jpg')
img = cv2.resize(img, (400, 500))
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("original image", img)

# Initialize face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
faces = detector(gray_img)

landmarkspints = []
for face in faces:
    x1, y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()
    landmarks = predictor(gray_img, face)

    # Plot landmarks
    for n in range(68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        landmarkspints.append([x, y])
        # cv2.circle(img, (x, y), 3, (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(n), (x + 0, y - 0), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 255), 1)

    landmarkspints = np.array(landmarkspints)
    eye_mask = np.zeros_like(img)

    # Extract landmarks for the left eye
    left_eye_indices = [39, 38, 37, 41, 40]  # Left eye only
    left_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in left_eye_indices],
                                  dtype=np.int32)

    # Separate upper and lower parts of the eye
    upper_left_eye = left_eye_landmarks[:3]  # Upper part
    lower_left_eye = left_eye_landmarks[3:]  # Lower part

    # Modify the lower part to stick at the bottom
    lower_left_eye[:, 1] -= 40

    # Combine upper and lower parts back
    left_eye_landmarks = np.vstack((upper_left_eye, lower_left_eye))

    # Define scaling factors for width (x-axis) and height (y-axis)
    scale_factor_x = 1.5
    scale_factor_y = 0.7

    # Calculate the center of the eye landmarks (both x and y)
    center_left = np.mean(left_eye_landmarks, axis=0)

    # Center the landmarks around the origin (subtract center)
    centered_landmarks = left_eye_landmarks - center_left

    # Apply scaling to x and y axes independently
    scaled_landmarks = np.zeros_like(centered_landmarks)
    scaled_landmarks[:, 0] = centered_landmarks[:, 0] * scale_factor_x  # Scale width
    scaled_landmarks[:, 1] = centered_landmarks[:, 1] * scale_factor_y  # Scale height

    # Shift the landmarks back to their original position (add center)
    left_eye_landmarks = (scaled_landmarks + center_left).astype(np.int32)

    left_eye_mask = cv2.fillPoly(eye_mask, [left_eye_landmarks], (255, 255, 255))

    # Extract landmarks for the right eye
    right_eye_indices = [42, 43, 44, 46, 47] # Right eye only
    right_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in right_eye_indices],
                                   dtype=np.int32)

    # Separate upper and lower parts of the eye
    upper_right_eye = right_eye_landmarks[:3]  # Upper part
    lower_right_eye = right_eye_landmarks[3:]  # Lower part

    # Modify the lower part to stick at the bottom
    lower_right_eye[:, 1] -= 40

    # Combine upper and lower parts back
    right_eye_landmarks = np.vstack((upper_right_eye, lower_right_eye))

    # Define scaling factors for width (x-axis) and height (y-axis)
    scale_factor_x = 1.6
    scale_factor_y = 0.7

    # Calculate the center of the eye landmarks (both x and y)
    center_right = np.mean(right_eye_landmarks, axis=0)

    # Center the landmarks around the origin (subtract center)
    centered_landmarks = right_eye_landmarks - center_right

    # Apply scaling to x and y axes independently
    scaled_landmarks = np.zeros_like(centered_landmarks)
    scaled_landmarks[:, 0] = centered_landmarks[:, 0] * scale_factor_x  # Scale width
    scaled_landmarks[:, 1] = centered_landmarks[:, 1] * scale_factor_y  # Scale height

    # Shift the landmarks back to their original position (add center)
    right_eye_landmarks = (scaled_landmarks + center_right).astype(np.int32)

    right_eye_mask = cv2.fillPoly(eye_mask, [right_eye_landmarks], (255, 255, 255))

    eye_mask = cv2.bitwise_or(left_eye_mask, right_eye_mask)

    # Define the color for the eyes
    eye_color = (0, 150, 255)  # Example color: Orange

    # Create a colored mask for the left eye
    eye_img_color = np.zeros_like(img)
    eye_img_color[:] = eye_color
    eye_img_color = cv2.bitwise_and(eye_mask, eye_img_color)

    eye_img_color = cv2.GaussianBlur(eye_img_color, (13, 13), 10)
    # eye_img_color = cv2.GaussianBlur(eye_img_color, (55, 45), 30)

    # Blend the original image with the colored eye masks
    final_makeup = cv2.addWeighted(img, 1, eye_img_color, 1, 0)

    # Show the final result
    cv2.imshow("final image", final_makeup)

cv2.waitKey(0)
cv2.destroyAllWindows()
