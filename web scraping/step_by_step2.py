import requests
from bs4 import BeautifulSoup
import csv
import time

def get_product_details(url):
    print(f"Fetching details from: {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    cpu = 'None'
    hardware_section = soup.select('div', id='code_block-745-114924')
    
    if hardware_section:
        rows = hardware_section.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                key = cols[0].text.strip().lower()
                value = cols[1].text.strip()
                if 'chipset' in key:
                    cpu = value
                    print(f"Found CPU: {cpu}")
                    break
    
    if cpu == 'None':
        print("CPU information not found")
    
    return cpu

base_url = "https://carisinyal.com/hp/?_sfm_harga_status=Available&_sfm_layar_ukuran_layar=1.77+14.61&_sfm_baterai_kapasitas_baterai=0+32000"

soup = BeautifulSoup(base_url.content, 'html.parser')
# Find all product containers
products = soup.select('div.oxy-post')  # Adjust this selector if needed
print(f"Found {len(products)} product containers on page {page_number}")

for product in products:
    name_elem = product.select_one('a.oxy-post-title')
    if name_elem:
        name = name_elem.text.strip()
        link = name_elem['href']
        price_elem = product.select_one('div.harga')
        price = price_elem.text.strip() if price_elem else 'N/A'

    try:
        # Get CPU info from the product page
        cpu = get_product_details(link)
    except Exception as e:
        print(f"Error fetching details for {name}: {str(e)}")
        cpu = 'Error'