import cv2
import dlib
import numpy as np

# Load the input image
img = cv2.imread('pic4.jpg')

# Resize the image
# img = cv2.resize(img, (300, 300))

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

    # Extract landmark points for the left and right areas of the cheeks
    left_cheek_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in left_cheek_indices], dtype=np.int32)
    right_cheek_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in right_cheek_indices], dtype=np.int32)

    # Scale down the landmarks by 20%
    scale_factor = 0.7
    center_left = np.mean(left_cheek_landmarks, axis=0)
    center_right = np.mean(right_cheek_landmarks, axis=0)
    left_cheek_landmarks = ((left_cheek_landmarks - center_left) * scale_factor + center_left).astype(np.int32)
    right_cheek_landmarks = ((right_cheek_landmarks - center_right) * scale_factor + center_right).astype(np.int32)

    # Create masks for the left and right areas of the cheeks
    left_cheek_mask = np.zeros_like(img)
    left_cheek_mask = cv2.fillPoly(left_cheek_mask, [left_cheek_landmarks], (255, 255, 255))

    right_cheek_mask = np.zeros_like(img)
    right_cheek_mask = cv2.fillPoly(right_cheek_mask, [right_cheek_landmarks], (255, 255, 255))

    # Combine the left and right cheek masks
    cheek_mask = cv2.bitwise_or(left_cheek_mask, right_cheek_mask)

    # Define the color for the cheeks
    cheek_color = (0, 150, 255)  # Example color: Orange

    # Create a colored mask for the cheeks
    cheek_img_color = np.zeros_like(img)
    cheek_img_color[:] = cheek_color
    cheek_img_color = cv2.bitwise_and(cheek_mask, cheek_img_color)
    cheek_img_color = cv2.GaussianBlur(cheek_img_color, (7, 7), 10)

    # Blend the original image with the colored cheek mask
    final_makeup_cheek = cv2.addWeighted(img, 1, cheek_img_color, 0.6, 0)

    cv2.imshow("final image cheek", final_makeup_cheek)

# Wait for a key press and then close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()
