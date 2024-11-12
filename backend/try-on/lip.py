import cv2
import dlib
import numpy as np
# import matplotlib.pyplot as plt

img = cv2.imread('pic4.jpg')
# img = cv2.resize(img, (300,300))
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# cv2.imshow("gray image", gray_img)
cv2.imshow("original image", img)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
faces = detector(gray_img)
print (faces)

landmarkspints = []
for face in faces:
    x1,y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()
    # img = cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),3)
    # cv2.imshow("face detected", img)
    landmarks = predictor(gray_img,face)
    for n in range(68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        landmarkspints.append([x,y])
        # show จุดละเลขบนหน้า
        cv2.circle(img,(x,y),3,(0,255,0),cv2.FILLED)
        cv2.putText(img,str(n), (x+10,y-10), cv2.FONT_HERSHEY_PLAIN,0.5,(0,0,255),1)
    landmarkspints = np.array(landmarkspints)
    lipmask = np.zeros_like(img)
    lipimg = cv2.fillPoly(lipmask, [landmarkspints[48:64]],(255,255,255))
    # cv2.imshow("lip",lipimg)
    # cv2.imshow("face landmark", img)

    lipimgcolor = np.zeros_like(lipimg)
    b = 200
    g = 20
    r = 70
    lipimgcolor[:] = b,g,r
    lipimgcolor = cv2.bitwise_and(lipimg,lipimgcolor)
    lipimgcolor = cv2.GaussianBlur(lipimgcolor, (7,7),10)

    finalmakeup = cv2.addWeighted(img,1,lipimgcolor,0.6,0)
    cv2.imshow("final image", finalmakeup)


cv2.waitKey(0)