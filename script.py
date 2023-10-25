import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.ebay.com/globaldeals/tech/cell-phones"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

response_text = requests.get(url, headers=headers).text

soup = BeautifulSoup(response_text, 'lxml')

# Initialize an empty list to store product information
products = []

all_product_div = soup.find_all(class_="col")
for product_div in all_product_div:
    price_element = product_div.find(class_="first")
    description_element = product_div.find("h3")
    link_element = product_div.find("a")

    product_price = price_element.text
    product_description = description_element.text
    product_link = link_element['href']

    # Store the product information in a dictionary
    product_info = {
        "Link": product_link,
        "Price": product_price,
        "Description": product_description
    }

    # Add the dictionary to the list of products
    products.append(product_info)

# Specify the name of the CSV file
csv_file = "products.csv"

# Open the CSV file in write mode and write the header
with open(csv_file, 'w', newline='') as file:
    fieldnames = ["Link", "Price", "Description"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Write each product's information to the CSV file
    for product in products:
        writer.writerow(product)

print(f"Product information has been saved to {csv_file}")