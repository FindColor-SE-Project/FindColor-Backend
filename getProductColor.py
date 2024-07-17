import cv2
import numpy as np
import urllib.request

def create_bar(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]),  int(color[0])
    return bar, (red, green, blue)

# ใส่ลิ้งค์ภาพตรงนี้
url = "https://s2.konvy.com/static/team_related/2023/0627/16878618075811.jpg"

# Download the image from the URL
req = urllib.request.urlopen(url)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

# Decode the image
img = cv2.imdecode(arr, -1)
img = cv2.resize(img,(400,400))
height, width, _ = np.shape(img)

data = np.reshape(img, (height * width, 3))
data = np.float32(data)

# ใส่ว่าเอากี่สีตรงนี้
number_clusters = 2
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
flags = cv2.KMEANS_RANDOM_CENTERS
compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)

bars = []
rgb_values = []

for index, row in enumerate(centers):
    bar, rgb = create_bar(200, 200, row)
    bars.append(bar)
    rgb_values.append(rgb)

img_bar = np.hstack(bars)

print(rgb_values)
cv2.imshow('Image', img)
cv2.imshow('Dominant colors', img_bar)
cv2.waitKey(0)

