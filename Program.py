from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import requests
import schedule
import time

# product object containing name, product link, and price
class ProductInfo:
    def __init__(self, product_name, product_link, product_price):
        self.productName = product_name
        self.productLink = product_link
        self.productPrice = product_price

# array of product objects
ProductList = []


# get webpage html, get products from page
def parse_to_products():
    request = requests.get("https://www.jetpens.com/cPath/new")
    soup = BeautifulSoup(request.text, "html.parser")
    product_listing = soup.find_all(class_="pure-u-1-2 pure-u-sm-1-2 pure-u-md-1-3 pure-u-lg-1-4 product")

    for item in product_listing:
        product = item.find_next(class_="product-name subtle").text
        link = item.find_next(class_="product-name subtle")["href"]
        price = item.find_next(class_="price").text
        ProductList.append(ProductInfo(product, link, price))

    for obj in ProductList:
        print(obj.productName)
        print(obj.productLink)
        print(obj.productPrice)


# create rss feed from product array
def products_to_xml():
    fg = FeedGenerator()
    fg.title("JetPens New Arrivals")
    fg.link(href="url")
    fg.description("New Arrivals from JetPens")
    for obj in reversed(ProductList):
        fe = fg.add_entry()
        fe.title(obj.productName)
        fe.link(href=obj.productLink)
        fe.description(obj.productPrice)
    fg.rss_file("test.xml", pretty=True)


def run():
    parse_to_products()
    products_to_xml()

# run program every day
schedule.every().day.at("00:00").do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
