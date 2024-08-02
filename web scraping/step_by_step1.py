import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://carisinyal.com/hp/?_sfm_harga_status=Available&_sfm_layar_ukuran_layar=1.77+14.61&_sfm_baterai_kapasitas_baterai=0+32000"

response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')
# Find all product containers
products = soup.select('div.oxy-post')  # Adjust this selector if needed

for product in products:
    name_elem = product.select_one('a.oxy-post-title')
    if name_elem:
        name = name_elem.text.strip()
        link = name_elem['href']
        price_elem = product.select_one('div.harga')
        price = price_elem.text.strip() if price_elem else 'N/A'
    print(name, link, price)
