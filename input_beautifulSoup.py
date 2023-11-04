import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import time

# Function to connect to a website and scrape the price
def connect_to_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to scrape Amazon and Flipkart prices
def scrape_prices(amazon_url, flipkart_url):
    amazon_html = connect_to_website(amazon_url)
    flipkart_html = connect_to_website(flipkart_url)

    if amazon_html and flipkart_html:
        amazon_soup = BeautifulSoup(amazon_html, 'html.parser')
        amazon_price_element = amazon_soup.find("span", {"class": "a-price-whole"})
        amazon_price = amazon_price_element.text.strip() if amazon_price_element else "Not found on Amazon"

        flipkart_soup = BeautifulSoup(flipkart_html, 'html.parser')
        flipkart_price_element = flipkart_soup.find("div", {"class": "_30jeq3 _16Jk6d"})
        flipkart_price = flipkart_price_element.text.strip().lstrip("₹") if flipkart_price_element else "Not found on Flipkart"

        return amazon_price, flipkart_price
    else:
        return "Failed to retrieve Amazon", "Failed to retrieve Flipkart"

# Function to display the prices in the GUI
def display_prices():
    amazon_url = amazon_url_entry.get()
    flipkart_url = flipkart_url_entry.get()
    amazon_price, flipkart_price = scrape_prices(amazon_url, flipkart_url)
    amazon_statement = f"Price on Amazon: {amazon_price}"
    flipkart_statement = f"Price on Flipkart: {flipkart_price}"
    result_label.config(text=f"{amazon_statement}\n{flipkart_statement}\n\nNOTE: Prices are in INR")

# Create the main window
root = tk.Tk()
root.title("Price Comparison")

# Set the default size of the window (width x height)
root.geometry("400x200")

# Set the background color for the main window
root.configure(bg="#f2f2f2")

# Create labels and entry fields for Amazon and Flipkart URLs
amazon_url_label = tk.Label(root, text="Amazon URL:")
amazon_url_label.pack()
amazon_url_entry = tk.Entry(root, width=40)
amazon_url_entry.pack()

flipkart_url_label = tk.Label(root, text="Flipkart URL:")
flipkart_url_label.pack()
flipkart_url_entry = tk.Entry(root, width=40)
flipkart_url_entry.pack()

# Create a button to trigger the price comparison
compare_button = tk.Button(root, text="Compare Prices", command=display_prices)
compare_button.pack(pady=10)

# Create a label to display the results
result_label = tk.Label(root, text="NOTE: Prices are in INR", wraplength=400)
result_label.pack()

root.mainloop()
