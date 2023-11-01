import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_data(url):
    response_text = requests.get(url).text
    soup = BeautifulSoup(response_text, 'lxml')
    all_product_card = soup.find_all(class_="card-body")

    # Initialize an empty list to store product information
    products = []

    for product_card in all_product_card:
        product_title = product_card.find(class_="title").text
        product_price = product_card.find(class_="price").text
        product_description = product_card.find(class_="description").text

        # Store the product information in a dictionary
        product_info = {
            "Title": product_title,
            "Price": product_price,
            "Description": product_description
        }

        # Add the dictionary to the list of products
        products.append(product_info)

    return products

def save_product_data_to_csv(products, csv_file):
    with open(csv_file, 'w', newline='') as file:
        fieldnames = ["Title", "Price", "Description"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Write each product's information to the CSV file
        for product in products:
            writer.writerow(product)

    print(f"Product information has been saved to {csv_file}")

# Specify the URL to scrape
url = "https://webscraper.io/test-sites/e-commerce/allinone"

# Call the scrape_product_data function to fetch and process the data
product_data = scrape_product_data(url)

# Specify the name of the CSV file
csv_file = "products.csv"

# Call the save_product_data_to_csv function to save the data to a CSV file
save_product_data_to_csv(product_data, csv_file)
