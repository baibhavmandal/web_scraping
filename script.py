# Import the necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

# Set up the WebDriver (you may need to install the appropriate driver)
driver = webdriver.Chrome()  # Example for Chrome

url = "https://www.amazon.in/gp/most-wished-for/electronics/1805559031/ref=zg_mw_pg_1_electronics?ie=UTF8&pg=1"
driver.get(url)

product_grid_id = "gridItemRoot"

# Wait for all elements with the specified ID to be present
all_product_grid_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.ID, product_grid_id))
)

print(f'Total number of product: {len(all_product_grid_elements)}')

# Initialize lists to store data
all_data = []

for product_grid_element in all_product_grid_elements:
    product_grid_html = product_grid_element.get_attribute("outerHTML")

    soup = BeautifulSoup(product_grid_html, 'html.parser')

    product_links_class_name = "a-link-normal"
    product_links = soup.find_all(class_=product_links_class_name)
    links = []  # Use a list to store all links
    description = ""
    product_price_class_name = "a-color-price"
    product_price_element = soup.find(class_=product_price_class_name)
    product_price = ""

    if product_price_element is not None:
        product_price = product_price_element.text
        print(f'Price: {product_price}')
    else:
        print('Price element not found')

    for index, link_element in enumerate(product_links):
        href = link_element.get('href')
        text = link_element.text
        links.append(href)  # Store links in the list
        if index == 1:
            description = text

    print(f'Description: {description}')
    print(f'Links: {links}')

    data = [description, product_price] + links
    all_data.append(data)

# Clean up and close the WebDriver
driver.quit()

csv_file_name = "product_data.csv"

# Write the data to the CSV file
with open(csv_file_name, 'w', newline='', encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header row
    csv_writer.writerow(["Description", "Price"] + [f"Link {i}" for i in range(len(links))])
    
    # Write the data
    for data_row in all_data:
        csv_writer.writerow(data_row)