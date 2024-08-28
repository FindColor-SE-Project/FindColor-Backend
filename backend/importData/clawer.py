from bs4 import BeautifulSoup
import requests
import cv2
import numpy as np
import urllib.request


def get_product_detail(url) :
    product_detail = requests.get(url)
    soup = BeautifulSoup(product_detail.content, "html.parser")

    meta = soup.find('div', {'class': 'w1180 pro-title team_media1000 ky-text-regular ky-font'}).find_all('a')
    productName = soup.find('h1', {'class': 'ky-fw ky-d-ib'}).text
    productDescription = soup.find('div', {'class': 'product-narrow-style'}).find('span').text
    imageUrl = soup.find('img', {'class': 'hover_sm'})['src']

    colorUrl = ''
    try:
        colorUrl = soup.find('li', {'class': 'active'}).find('a').find('img')['src']
    except:
        print('No color from' + productName)

    productCategory = str(meta[2].text).strip()
    if "ปาก" in productCategory or "ลิป" in productCategory:
        productCategory = "Lips"
    elif "แก้ม" in productCategory or "บลัช" in productCategory or "เฟซ" in productCategory:
        productCategory = "Blush"
    elif "ตา" in productCategory or "อาย" in productCategory:
        productCategory = "Eyeshadow"
    else:
        print("can't define category in: ", productCategory)

    brandName = str(meta[1].text)
    brandLogo = soup.find('a', {'class': 'pro-logo ky-d-ib'})['style'].split("('", 1)[1].split("')")[0]

    number_clusters = get_number_clusters(brandName, productCategory)
    colorRGB = get_dominant_colors(colorUrl, number_clusters)

    return (
        productName,
        brandLogo,
        brandName,
        productCategory,
        str(colorRGB),
        imageUrl,
        productDescription
    )



# Function to create a color bar
def create_bar(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    return bar, (red, green, blue)


# Function to get RGB values from an image URL
def get_dominant_colors(url, number_clusters):
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
        # test color81 82 84 85 88-95
        bars = []
        for index, row in enumerate(centers):
            bar, rgb = create_bar(200, 200, row)
            bars.append(bar)
            rgb_values.append(rgb)

        img_bar = np.hstack(bars)

        # Display the image and the dominant colors
        # cv2.imshow('Image', img)
        # cv2.imshow('Dominant colors', img_bar)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return rgb_values
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return []

def get_number_clusters(brand, category):
    if brand == "4U2" and category == "Eyeshadow":
        number_clusters = 2
    elif brand == "CathyDoll" and category == "Eyeshadow":
        number_clusters = 3
    elif brand == "Sasi" and category == "Eyeshadow":
        number_clusters = 4
    elif brand == "2P" and category == "Blush":
        number_clusters = 2
    else:
        number_clusters = 1
    return number_clusters