import pandas as pd
import openpyxl
import re

file = r"Scrape/4U2/4U2Lip.xlsx"
df = pd.read_excel(file)

# ดึงข้อมูลจากชื่อ column
exCategory = list(df['Category_Brand'])
exLogo = list(df['Logo-src'])
exImage = list(df['img-src'])
exColor = list(df['color'])
exDescription = list(df['Description'])


# แก้ข้อมูลของ exCategory ให้เป็น (Lips, Blush หรือ Eyeshadow)
for i, element in enumerate(exCategory):
    if "ปาก" in element:
        exCategory[i] = "Lips"
    elif "แก้ม" in element:
        exCategory[i] = "Blush"
    elif "ตา" in element:
        exCategory[i] = "Eyeshadow"
    else:
        print(element)


# แยก name ออกจาก description
exName = []
for description in exDescription:
    match = re.search(r'^([A-Za-z0-9\s#.,&()-]+)', description)
    if match:
        exName.append(match.group(1).strip())
    else:
        exName.append("")

print("Extracted Names:", exName)

# ต้องแก้ exColor