from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import requests
import schedule
import time
import math
import uuid

# product object containing name, product link, and price
class ProductInfo:
    def __init__(self, product_name, product_link, product_price):
        self.productName = product_name
        self.productLink = product_link
        self.productPrice = product_price

# array of product objects
ProductStorage = []


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
        for item in new_products:
            product = item.find_next(class_="product-name subtle").text
            link = item.find_next(class_="product-name subtle")["href"]
            price = item.find_next(class_="price").text
            ProductStorage.append(ProductInfo(product, link, price))

        # advance page
        page = page + 1
        print(math.ceil(num_of_items / 48))
        print(page)
        # break when page count is equal to the rounded-up # of pages, found via dividing # of items by
        # items per page (48)
        if page == math.ceil(num_of_items / 48):
            break


# create rss file from product array
def new_arrivals_to_xml():
    new_arrivals_string = ""
    for obj in ProductStorage:
        new_arrivals_string += obj.productName + "<br>"
        new_arrivals_string += f"<a href=\"{obj.productLink}\"> Link to Product </a>" + "<br>"
        new_arrivals_string += obj.productPrice + "<br>"

    fg = FeedGenerator()
    fg.title("JetPens New Arrivals")
    fg.link(href="url")
    fg.description("New Arrivals from JetPens")

    fe = fg.add_entry()
    fe.title("New Arrivals from JetPens: " + datetime.today().strftime("%x"))
    fe.description("New Arrivals from JetPens: " + datetime.today().strftime("%x"))
    fe.content(new_arrivals_string)
    fe.guid(str(uuid.uuid4()))
    fg.rss_file("Feed.xml", pretty=True)

    print(new_arrivals_string)


def run():
    parse_to_products()
    new_arrivals_to_xml()


# run program every day
schedule.every().second.do(run)

# create xml on run
run()
while True:
    schedule.run_pending()
    time.sleep(1)
