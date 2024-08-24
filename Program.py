import bs4
import requests


class ProductInfo:
    productName = ""
    productPrice = ""

def get_html():
    request = requests.get("https://www.jetpens.com/cPath/new")
