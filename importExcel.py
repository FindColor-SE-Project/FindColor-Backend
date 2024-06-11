import pandas as pd
import openpyxl
import re
from bs4 import BeautifulSoup
import cv2
import numpy as np
import urllib.request

# Load the Excel file
file = r"Scrape/4U2/4U2Lip.xlsx"
df = pd.read_excel(file)

# ดึงข้อมูลจากชื่อ column
exCategory_Brand = list(df['Category_Brand'])
exLogo = list(df['Logo-src'])
exImage = list(df['img-src'])
exDescription = list(df['Description'])

# แก้ข้อมูลของ exCategory ให้เป็น (Lips, Blush หรือ Eyeshadow)
exCategory = []
for element in exCategory_Brand:
    if "ปาก" in element:
        exCategory.append("Lips")
    elif "แก้ม" in element:
        exCategory.append("Blush")
    elif "ตา" in element:
        exCategory.append("Eyeshadow")
    else:
        print(element)

# หาแบรนด์ใน exCategory_Brand และรวบรวมไว้ใน exBrand
exBrand = []
brands = ['2P', '4U2', 'CathyDoll', 'Laka', 'Sasi']

for element in exCategory_Brand:
    found_brand = None
    for brand in brands:
        if brand in element:
            found_brand = brand
            break
    if found_brand:
        exBrand.append(found_brand)
    else:
        exBrand.append(None)  # หรือสามารถใช้เป็น "" ได้ถ้าต้องการ

# แยก name ออกจาก description
exName = []
for description in exDescription:
    split_description = re.split(r'[\u0E00-\u0E7F]', description, maxsplit=1)
    exName.append(split_description[0].strip())

# Function to create a color bar
def create_bar(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    return bar, (red, green, blue)

# Function to get RGB values from an image URL
def get_dominant_colors(url, number_clusters=1):
    try:
        # Download the image from the URL
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

        # Decode the image
        img = cv2.imdecode(arr, -1)
        img = cv2.resize(img, (400, 400))
        height, width, _ = np.shape(img)

        data = np.reshape(img, (height * width, 3))
        data = np.float32(data)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)

        rgb_values = []
        for index, row in enumerate(centers):
            _, rgb = create_bar(200, 200, row)
            rgb_values.append(rgb)

        return rgb_values
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return []

# ดึง link รูปสีจาก color column และประมวลผลหา RGB
color_column = df['color']
exColor = []
exRGBcolor = []

for html_content in color_column:
    soup = BeautifulSoup(html_content, 'html.parser')
    active_image_links = [img['src'] for li in soup.find_all('li', class_='active') for img in li.find_all('img')]
    exColor.append(active_image_links)
    dominant_colors = []
    for link in active_image_links:
        dominant_colors.extend(get_dominant_colors(link))
    exRGBcolor.append(dominant_colors)

# Print the results
print("Categorized exCategory:", exCategory)
print("Found Brands:", exBrand)
print("Extracted Image Links:", exColor)
print("Extracted RGB values:", exRGBcolor)
print("Extracted Names:", exName)
