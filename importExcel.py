import pandas as pd
import openpyxl
import re
from bs4 import BeautifulSoup

file = r"Scrape/4U2/4U2Lip.xlsx"
df = pd.read_excel(file)

# ดึงข้อมูลจากชื่อ column
exCategory_Brand = list(df['Category_Brand'])
exLogo = list(df['Logo-src'])
exImage = list(df['img-src'])
exDescription = list(df['Description'])


# หาและแก้ข้อมูลของ exCategory ให้เป็น (Lips, Blush หรือ Eyeshadow)
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


# ดึง link รูปสีจาก color column
color_column = df['color']
exColor = []
for html_content in color_column:
    soup = BeautifulSoup(html_content, 'html.parser')
    active_image_links = [img['src'] for li in soup.find_all('li', class_='active') for img in li.find_all('img')]
    exColor.append(active_image_links)


print("Categorized exCategory:", exCategory)
print("Found Brands:", exBrand)
print("Extracted Image Links from 'active' class:", exColor)
print("Extracted Names:", exName)
