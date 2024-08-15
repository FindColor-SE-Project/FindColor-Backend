from bs4 import BeautifulSoup
import requests
import csv
import clawer

page_number = 1
previous_product_urls = []

while True:
    print('Page', page_number)
    raw_url = f'https://www.konvy.com/list/makeup/?filter_params=-1:3913,50,2998,4589,7337_-2:6992&page={page_number}'
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

    # Check if the current product URLs are the same as the previous ones
    if product_url_list == previous_product_urls:
        print('Reached the last page, ending scraping.')
        break

    product_data = []
    for prod_url in product_url_list:
        try:
            product_data.append(clawer.get_product_detail(prod_url))
        except Exception as e:
            print(f"Error processing URL {prod_url}: {e}")

    print(product_data)

    fields = ['brand', 'logo', 'category', 'name', 'description', 'image', 'color']

    # Name of csv file
    filename = f'{page_number}-product-list.csv'

    # Writing to csv file
    with open(filename, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(product_data)

    # Update the previous product URLs and increment the page number
    previous_product_urls = product_url_list
    page_number += 1
