from bs4 import BeautifulSoup
import requests
import csv
import clawer


for i in range(1,4):
    print('Page', i)
    raw_url = 'https://www.konvy.com/list/makeup/?filter_params=-1:50,3913,7337,2998,4589_-2:187&page=' + str(i)
    url = requests.get(raw_url)
    soup = BeautifulSoup(url.content, "html.parser")
    products = soup.find('ul', {'class': 'lise-row4 New_clear'}).find_all('li')
    # print(products)
    product_url_list = []
    for product in products:
        product_url = (product.find_all('a')[1]['href'])
        product_url_list.append(product_url)

    product_data = []

    for prod_url in product_url_list:
        product_data.append(clawer.get_product_detail(prod_url))

    print(product_data)

    fields = ['brand', 'logo', 'category', 'name', 'description', 'image', 'color']

    # name of csv file
    filename = f'{i}-product-list.csv'

    # writing to csv file
    with open(filename, 'w', encoding='utf-8') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(product_data)