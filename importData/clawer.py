from bs4 import BeautifulSoup
import requests


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
        print('No color')

    productCategory = str(meta[2].text).strip()
    brandName = str(meta[1].text)
    brandLogo = soup.find('a', {'class': 'pro-logo ky-d-ib'})['style'].split("('", 1)[1].split("')")[0]


    return {
        'brand': brandName,
        'logo': brandLogo,
        'category': productCategory,
        'name': productName,
        'description': productDescription,
        'image': imageUrl,
        'color': colorUrl
    }
# print("brand", brandName)
# print("logo", brandLogo)
# print("category", productCategory)
# print("name", productName)
# print("description", productDescription)
# print("img", imageUrl)
# print("color", colorUrl)

