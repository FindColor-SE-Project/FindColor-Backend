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
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Detect faces
    faces = detector(gray_img)
    if not faces:
        raise ValueError("No faces detected in the image.")

    # Process each detected face
    for face in faces:
        # Detect facial landmarks
        landmarks = predictor(gray_img, face)

        # Define cheek landmark indices
        left_cheek_indices = [0, 1, 2, 3, 31, 30, 29, 28, 27, 39, 40, 41, 36]
        right_cheek_indices = [13, 14, 15, 16, 45, 46, 47, 42, 27, 28, 29, 35]

        # Get landmarks for left and right cheeks
        left_cheek_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in left_cheek_indices],
                                        dtype=np.int32)
        right_cheek_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in right_cheek_indices],
                                         dtype=np.int32)

        # Scale landmarks down slightly for blush effect
        scale_factor = 0.6
        center_left = np.mean(left_cheek_landmarks, axis=0)
        center_right = np.mean(right_cheek_landmarks, axis=0)
        left_cheek_landmarks = ((left_cheek_landmarks - center_left) * scale_factor + center_left).astype(np.int32)
        right_cheek_landmarks = ((right_cheek_landmarks - center_right) * scale_factor + center_right).astype(np.int32)

        # Create cheek masks
        left_cheek_mask = np.zeros_like(img)
        right_cheek_mask = np.zeros_like(img)
        cv2.fillPoly(left_cheek_mask, [left_cheek_landmarks], (255, 255, 255))
        cv2.fillPoly(right_cheek_mask, [right_cheek_landmarks], (255, 255, 255))

        # Combine masks
        cheek_mask = cv2.bitwise_or(left_cheek_mask, right_cheek_mask)

        # Apply color to the cheek mask
        cheek_img_color = np.zeros_like(img)
        cheek_img_color[:] = cheek_color
        cheek_img_color = cv2.bitwise_and(cheek_mask, cheek_img_color)

        # Adjust cheek color saturation and brightness
        cheek_img_hsv = cv2.cvtColor(cheek_img_color, cv2.COLOR_BGR2HSV)
        cheek_img_hsv[:, :, 1] = np.clip(cheek_img_hsv[:, :, 1] * 1.5, 0, 255)
        cheek_img_hsv[:, :, 2] = np.clip(cheek_img_hsv[:, :, 2] * 0.5, 0, 255)
        cheek_img_color = cv2.cvtColor(cheek_img_hsv, cv2.COLOR_HSV2BGR)
        cheek_img_color = cv2.GaussianBlur(cheek_img_color, (25, 25), 35)

        # Blend the cheek color onto the original image
        final_makeup_cheek = cv2.addWeighted(img, 1, cheek_img_color, 0.8, 0)

    return final_makeup_cheek

# Load the image
img = cv2.imread('pic4.jpg')
if img is None:
    raise FileNotFoundError("The image file was not found.")

# Apply blush color
final_image = apply_blush_color(img, 254, 128, 175)

# Display the final image
cv2.imshow("Final Image with Cheek Makeup", final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
