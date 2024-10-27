import cv2
import dlib
import numpy as np

# Load the input image
img = cv2.imread('pic4.jpg')

# Resize the image
img = cv2.resize(img, (400, 500))

# Convert the image to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Display the original image
cv2.imshow("original image", img)

# Initialize the face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Detect faces in the grayscale image
faces = detector(gray_img)
print("rectangles", faces)

# Iterate over detected faces
for face in faces:
    # Get the coordinates of the bounding box
    x1, y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()

    # Detect facial landmarks
    landmarks = predictor(gray_img, face)

    # Define the indices for the left and right areas of the cheeks
    left_cheek_indices = [0, 1, 2, 3, 31, 30, 29, 28, 27, 39, 40, 41, 36]
    right_cheek_indices = [13, 14, 15, 16, 45, 46, 47, 42, 27, 28, 29, 35]
    left_eye_indices = [36, 37, 38, 39, 40, 41]
    right_eye_indices = [42, 43, 44, 45, 46, 47]

    # Extract landmark points for the left and right areas of the cheeks
    left_cheek_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in left_cheek_indices], dtype=np.int32)
    right_cheek_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in right_cheek_indices], dtype=np.int32)

    # Scale down the landmarks by 20%
    scale_factor = 0.6
    center_left = np.mean(left_cheek_landmarks, axis=0)
    center_right = np.mean(right_cheek_landmarks, axis=0)
    left_cheek_landmarks = ((left_cheek_landmarks - center_left) * scale_factor + center_left).astype(np.int32)
    right_cheek_landmarks = ((right_cheek_landmarks - center_right) * scale_factor + center_right).astype(np.int32)
    left_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in left_eye_indices], dtype=np.int32)
    right_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in right_eye_indices], dtype=np.int32)

    # Create masks for the left and right areas of the cheeks
    left_cheek_mask = np.zeros_like(img)
    left_cheek_mask = cv2.fillPoly(left_cheek_mask, [left_cheek_landmarks], (255, 255, 255))

    right_cheek_mask = np.zeros_like(img)
    right_cheek_mask = cv2.fillPoly(right_cheek_mask, [right_cheek_landmarks], (255, 255, 255))

    # Combine the left and right cheek masks
    cheek_mask = cv2.bitwise_or(left_cheek_mask, right_cheek_mask)

    # Create eye masks
    left_eye_mask = np.zeros_like(img)
    right_eye_mask = np.zeros_like(img)

    cv2.fillPoly(left_eye_mask, [left_eye_landmarks], (255, 255, 255))
    cv2.fillPoly(right_eye_mask, [right_eye_landmarks], (255, 255, 255))

    # Combine eye masks
    eye_mask = cv2.bitwise_or(left_eye_mask, right_eye_mask)

    # Define the color for the cheeks
    cheek_color = (254, 133, 132)  # Example cheek color (soft pink)

    # Create a colored mask for the cheeks
    cheek_img_color = np.zeros_like(img)
    cheek_img_color[:] = cheek_color
    cheek_img_color = cv2.bitwise_and(cheek_mask, cheek_img_color)

    # Convert cheek color image to HSV
    cheek_img_hsv = cv2.cvtColor(cheek_img_color, cv2.COLOR_BGR2HSV)

    # Adjust the saturation and brightness in the HSV space
    saturation_factor = 1.8  # Increase saturation
    brightness_factor = 1  # Increase brightness

    # Apply the adjustments (clip to valid range: 0-255)
    cheek_img_hsv[:, :, 1] = np.clip(cheek_img_hsv[:, :, 1] * saturation_factor, 0, 255)  # Saturation
    cheek_img_hsv[:, :, 2] = np.clip(cheek_img_hsv[:, :, 2] * brightness_factor, 0, 255)  # Brightness

    # Convert the modified HSV image back to BGR
    cheek_img_color = cv2.cvtColor(cheek_img_hsv, cv2.COLOR_HSV2BGR)

    # Apply Gaussian blur to smooth the edges
    cheek_img_color = cv2.GaussianBlur(cheek_img_color, (25, 25), 35)

    eye_mask_gray = cv2.cvtColor(eye_mask, cv2.COLOR_BGR2GRAY)
    _, eye_mask_binary = cv2.threshold(eye_mask_gray, 1, 255, cv2.THRESH_BINARY)
    # final_cheek_mask = cv2.inpaint(cheek_img_color, eye_mask_binary, 5, cv2.INPAINT_TELEA)

    final_cheek_mask = cv2.subtract(cheek_img_color, eye_mask)

    # Blend the original image with the adjusted cheek mask
    final_makeup_cheek = cv2.addWeighted(img, 1, final_cheek_mask, 0.5, 0)

    # Display the final image with cheek makeup
    cv2.imshow("final image cheek", final_makeup_cheek)

# Wait for a key press and then close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()
