import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('pic4.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("original image", img)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
faces = detector(gray_img)
print (faces)

landmarkspints = []
for face in faces:
    x1, y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()
    landmarks = predictor(gray_img, face)
    for n in range(68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        landmarkspints.append([x, y])
        cv2.circle(img,(x,y),3,(0,255,0),cv2.FILLED)
        cv2.putText(img,str(n), (x+10,y-10), cv2.FONT_HERSHEY_PLAIN,0.5,(0,0,255),1)
    landmarkspints = np.array(landmarkspints)
    eye_mask = np.zeros_like(img)

    # Extract landmarks for the left eye
    left_eye_indices = [36, 37, 38, 39, 21, 20, 19, 18, 17]
    left_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in left_eye_indices], dtype=np.int32)
    left_eye_landmarks_center = np.mean(left_eye_landmarks, axis=0)
    left_eye_landmarks[:, 1] = ((left_eye_landmarks[:, 1] - left_eye_landmarks_center[1]) * 0.6 + left_eye_landmarks_center[1])
    left_eye_img = cv2.fillPoly(eye_mask, [left_eye_landmarks], (255, 255, 255))

    # Extract landmarks for the right eye
    right_eye_indices = [42, 43, 44, 45, 26, 25, 24, 23, 22]
    right_eye_landmarks = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in right_eye_indices], dtype=np.int32)
    right_eye_landmarks_center = np.mean(right_eye_landmarks, axis=0)
    right_eye_landmarks[:, 1] = ((right_eye_landmarks[:, 1] - right_eye_landmarks_center[1]) * 0.6 + right_eye_landmarks_center[1])
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

    cv2.imshow("final image", final_makeup)

cv2.waitKey(0)
cv2.destroyAllWindows()
