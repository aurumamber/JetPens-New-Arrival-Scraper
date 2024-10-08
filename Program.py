from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import requests
import schedule
import time
import math
import uuid
import pickle
import os.path

# product class
class ProductInfo:
    def __init__(self, product_name, product_link, product_price):
        self.productName = product_name
        self.productLink = product_link
        self.productPrice = product_price

    def __eq__(self, other):
        return (self.productName == other.productName and
                self.productLink == other.productLink and
                self.productPrice == other.productPrice)

    def __hash__(self):
        return hash((self.productName, self.productLink, self.productPrice))


# lists of product objects
ProductComparison = []
ProductStorage = []
# MAKE A COMPARISON ARRAY. COMPARE PRODUCT STORAGE AND THE COMPARISON ARRAY.
# IF THEY MATCH 1:1, DO NOT MAKE A NEW FEED ENTRY.
# IF ONLY SOME OF THE ITEMS MATCH, REMOVE THE MATCHING ITEMS, THEN COPY REMAINDER TO PRODUCT STORAGE AND
# MAKE NEW ENTRY.

def compare_to_storage():
    if ProductComparison == ProductStorage:
        with open("product_storage", "wb") as fp:
            pickle.dump(ProductStorage, fp)
        return True
    else:
        for item in ProductComparison:
            if item in ProductStorage:
                ProductStorage.remove(item)
            else:
                ProductStorage.append(item)
        with open("product_storage", "wb") as fp:
            pickle.dump(ProductStorage, fp)
        return False


# get webpage html, get new products from page
def parse_to_products():
    page = 1
    while True:
        url = f"https://www.jetpens.com/cPath/new?pn={page}"
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")
        # get amount of items, to divide by items per page and find # of pages
        num_of_items = int(soup.find(class_="pure-u-1-4 display-sm-none").text.strip("items"))
        new_products = soup.find_all(class_=["pure-button product-image-tag new",
                                             "pure-button product-image-tag limited"])
        # add items to list
        for item in new_products:
            product = item.find_next(class_="product-name subtle").text
            link = item.find_next(class_="product-name subtle")["href"]
            price = item.find_next(class_="price").text
            if ProductInfo(product, link, price) not in ProductComparison:
                ProductComparison.append(ProductInfo(product, link, price))

        # advance page
        page += 1
        print(page)
        # break when page count is equal to the rounded-up # of pages, found via dividing # of items by
        # items per page (48)
        if page == math.ceil(num_of_items / 48):
            break

def create_feed():
    fg = FeedGenerator()
    fg.title("JetPens New Arrivals")
    fg.link(href="url")
    fg.description("New Arrivals from JetPens")
    fg.rss_file("Feed.xml")
    with open("feed", "wb") as f:
        pickle.dump(fg, f)
    print("guess we doin feeds now")


# create rss file from product list
def new_arrivals_to_feed():
    # create feed if it doesn't exist
    if not os.path.isfile("Feed.xml"):
        create_feed()

    # content
    new_arrivals_string = ""
    for item in ProductStorage:
        new_arrivals_string += "<tr>\n<td>" + item.productName + "</td>"
        new_arrivals_string += "<td>\n" + f"<a href=\"{item.productLink}\"> Link to Product </a>" + "</td>"
        new_arrivals_string += "<td>\n" + item.productPrice + "</td>"
    new_arrivals_string = ("<table>\n<tr>\n<th>Product</th>\n<th>Link</th>\n<th>Price</th>"
                           + new_arrivals_string
                           + "</tr>\n<table>")

    # add entries
    with open("feed", "rb") as f:
        fg = pickle.load(f)
        fe = fg.add_entry()
        fe.title("New Arrivals from JetPens: " + datetime.today().strftime("%c"))
        fe.description("New Arrivals from JetPens: " + datetime.today().strftime("%c"))
        fe.content(new_arrivals_string)
        fe.guid(str(uuid.uuid4()))
        fg.rss_file("Feed.xml", pretty=True)
       # print(new_arrivals_string)
    with open("feed", "wb") as f:
        pickle.dump(fg, f)


def run():
    parse_to_products()
    if not compare_to_storage():
        new_arrivals_to_feed()


# run program every day
schedule.every().day.at("00:00").do(run)

# create xml on run
if os.path.isfile("product_storage"):
    with open("product_storage", "rb") as fp:
        ps = pickle.load(fp)
        ProductStorage = ps
run()
while True:
    schedule.run_pending()
    time.sleep(1)
