from bs4 import BeautifulSoup
import requests
import clawer

# List of URLs to scrape
url_list = [
    # 'https://www.konvy.com/list/makeup/?filter_params=-1:50,2998,3913,7337,4589_-2:187',
    # 'https://www.konvy.com/list/makeup/?filter_params=-1:50,3913,2998,7337,4589_-2:1101',
    # 'https://www.konvy.com/list/makeup/?filter_params=-1:50,2998,3913,4589,7337_-2:185',
    # 'https://www.konvy.com/list/makeup/?filter_params=-1:50,3913,2998,7337,4589_-2:188',
    # 'https://www.konvy.com/list/makeup/?filter_params=-1:50,3913,4589,2998,7337_-2:6992',
    'https://www.konvy.com/list/makeup/?filter_params=-1:50,2998,4589,7337,3913_-2:180'
]

# List to store all validated product data
all_products = []

for url_index, base_url in enumerate(url_list):
    print(f'Scraping URL {url_index + 1}: {base_url}')
    page_number = 1
    previous_product_urls = []

    while True:
        print('Page', page_number)
        raw_url = f'{base_url}&page={page_number}'
        response = requests.get(raw_url)
        soup = BeautifulSoup(response.content, "html.parser")

        products = soup.find('ul', {'class': 'lise-row4 New_clear'}).find_all('li')
        if not products:
            print('No more products found, ending scraping.')
            break

        product_url_list = [product.find_all('a')[1]['href'] for product in products]

        # Check if the current product URLs are the same as the previous ones
        if product_url_list == previous_product_urls:
            print('Reached the last page, ending scraping.')
            break

        product_data = []
        for prod_url in product_url_list:
            try:
                product = clawer.get_product_detail(prod_url)
                if product:  # Only add valid products
                    product_data.append(product)
                else:
                    print(f"Skipping invalid product from URL: {prod_url}")
            except Exception as e:
                print(f"Error processing URL {prod_url}: {e}")

        print(f"Products added from page {page_number}: {len(product_data)}")

        # Add validated products to all_products
        all_products.extend(product_data)
        previous_product_urls = product_url_list
        page_number += 1

print("Total valid products scraped:", len(all_products))

def all_product_number():
    return len(all_products)

def get_product():
    return all_products
