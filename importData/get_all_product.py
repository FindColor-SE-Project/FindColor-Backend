from bs4 import BeautifulSoup
import requests
import csv
import clawer

page_number = 1

while True:
    print('Page', page_number)
    raw_url = f'https://www.konvy.com/list/makeup/?filter_params=-1:50,3913,7337,2998,4589_-2:187&page={page_number}'
    url = requests.get(raw_url)
    soup = BeautifulSoup(url.content, "html.parser")

    products = soup.find('ul', {'class': 'lise-row4 New_clear'}).find_all('li')

    if not products:
        print('No more products found, ending scraping.')
        break

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
    filename = f'{page_number}-product-list.csv'

    # writing to csv file
    with open(filename, 'w', encoding='utf-8') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(product_data)

    page_number += 1
