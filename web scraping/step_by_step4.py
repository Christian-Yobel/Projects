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
total_pages = 32
all_products = []

for page_number in range(1, total_pages + 1):
    url = base_url if page_number == 1 else f"{base_url}&sf_paged={page_number}"
    print(f"Scraping page {page_number} of {total_pages}")
    print(f"URL: {url}")
    
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

        all_products.append({
            "name": name,
            "price": price,
            "cpu": cpu,
            "link": link
        })
                
        print(f"Scraped: {name}")
                
        # Add a delay to be respectful to the server
        time.sleep(2)
    else:
        print(f"Couldn't find name for a product")
    
    # Add a delay between pages
    time.sleep(5)

print(f"Successfully scraped {len(all_products)} products in total")

# Write to CSV
if all_products:
    keys = all_products[0].keys()
    with open('all_products_with_cpu.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_products)
    print("CSV file created successfully.")
else:
    print("No products found. The scraping might have failed.")