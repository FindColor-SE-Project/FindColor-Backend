import pandas as pd

file = r"Scrape/4U2/4U2Lip.xlsx"

df = pd.read_excel(file)

exCategory = list(df['Category_Brand'])
exLogo = list(df['Logo-src'])
exImage = list(df['img-src'])
exColor = list(df['color'])
exDescription = list(df['Description'])

print(exCategory)

