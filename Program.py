from bs4 import BeautifulSoup
import requests


class ProductInfo:
    def __init__(self, productname, productprice):
        self.productName = productname
        self.productPrice = productprice


ProductList = []

def parse_html():
    request = requests.get("https://www.jetpens.com/cPath/new")
    soup = BeautifulSoup(request.text,"html.parser")

    for item in soup.find_all(class_="pure-u-1-2 pure-u-sm-1-2 pure-u-md-1-3 pure-u-lg-1-4 product"):
        product = item.find_next(class_="product-name subtle").text
        price = item.find_next(class_="price").text
        ProductList.append(ProductInfo(product, price))
    for obj in ProductList:
        print(obj.productName)
        print(obj.productPrice)


parse_html()

