import httpx
from selectolax.parser import HTMLParser
import json
from rich import print
from dataclasses import dataclass

@dataclass
class Store:
    name: str
    url: str
    title: str
    price: str

@dataclass
class Item:
    store: Store
    title: str
    price: str
    
def load_stores():
    with open("links.json" , "r") as f:
        data = json.load(f)
    return [Store(**item) for item in data]

    
def load_page(client,url):
    resp=client.get(url)
    return HTMLParser(resp.text)

def parse(store, html):
    return Item(store=store, title=html.css_first(store.title).text(strip=True),price=html.css_first(store.price).text(strip=True))

def store_selector(stores, url):
    for store in stores:
        if store.url in url:
            return store

def main():
    stores = load_stores()
    print(stores)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    client = httpx.Client(headers=headers)
    
    urls = [
        "https://rab.equipment",
        "https://blackdiamondequipment.com/"
    ]
    
    for url in urls:
        store = store_selector(stores,url)
        html = load_page(client,url)
        print(parse(store,html))

if __name__ == "__main__":
    main()