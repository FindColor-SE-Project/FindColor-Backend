import cv2
from backend.try_on.blushTryOnGenerate import apply_blush_color
from backend.try_on.lipsTryOnGenerate import apply_lips_color
from backend.try_on.eyeshadowTryOnGenerate import apply_eyeshadow_color

img = cv2.imread('pic1.jpg')
if img is None:
    raise FileNotFoundError("The image file was not found.")

img = cv2.resize(img, (400,500))

final_image = apply_eyeshadow_color(img, 254, 128, 175)

cv2.imshow("Original Image", img)
cv2.imshow("Final Image", final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
