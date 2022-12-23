import csv
import requests
from bs4 import BeautifulSoup

list_of_urls = [
    'https://www.chocolate.co.uk/collections/all',
        ]

scraped_data = []

## Scraping Function
def start_scrape():
    
    ## Loop Through List of URLs
    for url in list_of_urls:
        
        ## Send Request
        response = requests.get(url)
        
        if response.status_code == 200:
            
            ## Parse Data
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.select('product-item')
            for product in products:
                name = product.select('a.product-item-meta__title')[0].get_text()
                price = product.select('span.price')[0].get_text().replace('\nSale price£', '')
                url = product.select('div.product-item-meta a')[0]['href']
                
                ## Add To Data Output
                scraped_data.append({
                    'name': name,
                    'price': price,
                    'url': 'https://www.chocolate.co.uk' + url
                })
            
            ## Next Page
            next_page = soup.select('a[rel="next"]')
            if len(next_page) > 0:
                list_of_urls.append('https://www.chocolate.co.uk' + next_page[0]['href'])


def save_to_csv(data_list, filename):
    keys = data_list[0].keys()
    with open(filename + '.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data_list)
        
if __name__ == "__main__":
    start_scrape()
    save_to_csv(scraped_data, 'scraped_data')
    
    