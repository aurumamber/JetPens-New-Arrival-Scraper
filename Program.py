import bs4
from bs4 import BeautifulSoup
import requests


class ProductInfo:
    productName = ""
    productPrice = ""


def parse_html():
    request = requests.get("https://www.jetpens.com/cPath/new")
    soup = BeautifulSoup(request.text,"html.parser")
    arrival_text = soup.find("div", {"class" : "products pure-g margin-tb-10"})
    print(arrival_text)


parse_html()

