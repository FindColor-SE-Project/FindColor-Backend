import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt

# Load the image
img = cv2.imread('pic4.jpg')
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
        cv2.circle(img, (x, y), 3, (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(n), (x + 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 255), 1)

    landmarkspints = np.array(landmarkspints)
    eye_mask = np.zeros_like(img)

    # Extract landmarks for the left eye
    left_eye_indices = [36, 37, 38, 39, 40, 41]  # Left eye only
    left_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in left_eye_indices],
                                  dtype=np.int32)

    # Separate upper and lower parts of the eye
    upper_left_eye = left_eye_landmarks[:3]  # Upper part
    lower_left_eye = left_eye_landmarks[3:]  # Lower part

    # Modify the lower part to stick at the bottom
    lower_left_eye[:, 1] -= 30  # Move lower part down by 10 pixels (you can adjust this)

    # Combine upper and lower parts back
    left_eye_landmarks = np.vstack((upper_left_eye, lower_left_eye))

    left_eye_img = cv2.fillPoly(eye_mask, [left_eye_landmarks], (255, 255, 255))

    # Extract landmarks for the right eye
    right_eye_indices = [42, 43, 44, 45, 46, 47]  # Right eye only
    right_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in right_eye_indices],
                                   dtype=np.int32)

    # Separate upper and lower parts of the eye
    upper_right_eye = right_eye_landmarks[:3]  # Upper part
    lower_right_eye = right_eye_landmarks[3:]  # Lower part

    # Modify the lower part to stick at the bottom
    lower_right_eye[:, 1] -= 30  # Move lower part down by 10 pixels

    # Combine upper and lower parts back
    right_eye_landmarks = np.vstack((upper_right_eye, lower_right_eye))

    right_eye_img = cv2.fillPoly(eye_mask, [right_eye_landmarks], (255, 255, 255))

    # Define the color for the eyes
    eye_color = (0, 150, 255)  # Example color: Orange

    # Create a colored mask for the left eye
    left_eye_color = np.zeros_like(img)
    left_eye_color[:] = eye_color
    left_eye_color = cv2.bitwise_and(left_eye_img, left_eye_color)

    # Create a colored mask for the right eye
    right_eye_color = np.zeros_like(img)
    right_eye_color[:] = eye_color
    right_eye_color = cv2.bitwise_and(right_eye_img, right_eye_color)

    # Blend the original image with the colored eye masks
    final_makeup = cv2.addWeighted(img, 1, left_eye_color + right_eye_color, 1, 0)

    # Show the final result
    cv2.imshow("final image", final_makeup)

cv2.waitKey(0)
cv2.destroyAllWindows()
