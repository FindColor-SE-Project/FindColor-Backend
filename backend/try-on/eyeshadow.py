import cv2
import dlib
import numpy as np

# Load the image and prepare it
img = cv2.imread('pic4.jpg')
img = cv2.resize(img, (400, 500))
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Initialize the face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
faces = detector(gray_img)

# Iterate over all detected faces
for face in faces:
    landmarks = predictor(gray_img, face)

    # Create a mask for the eyeshadow
    eye_mask = np.zeros_like(img)

    def create_eyeshadow_mask(indices, height_offset):
        """
        Function to create an eyeshadow mask by adding height only on the upper side.
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

    # Create masks for both eyes, adding height only to the upper side
    create_eyeshadow_mask([36, 37, 38, 39], height_offset=15)  # Left eye
    create_eyeshadow_mask([42, 43, 44, 45], height_offset=15)  # Right eye

    # Define the eyeshadow color (light purple in this case)
    eyeshadow_color = (180, 70, 255)

    # Create a colored mask with the eyeshadow color
    eyeshadow = np.zeros_like(img)
    eyeshadow[:] = eyeshadow_color

    # Apply the eyeshadow only where the mask is present
    colored_mask = cv2.bitwise_and(eyeshadow, eye_mask)

    # Blur the mask for smoother blending
    blurred_mask = cv2.GaussianBlur(colored_mask, (15, 15), 10)

    # Blend the original image with the blurred eyeshadow mask
    final_image = cv2.addWeighted(img, 1, blurred_mask, 0.5, 0)

    # Display the final result
    cv2.imshow("Eyeshadow Try-On", final_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
