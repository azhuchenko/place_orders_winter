import requests
import json
from config import get_ip, get_mfc_code

def get_stock_url(env):
    ip = get_ip(env)
    mfc_code = get_mfc_code(env)
    return f"http://{ip}:8090/api/stock/details?mfc-code={mfc_code}"

def get_stock(env, file="stock_list.txt"):
    with open(file, "r+") as stock:
        stock.truncate(0)
    url = get_stock_url(env)
    data = requests.get(url=url).json()
    stock_count = 0

    for record in data:
        if record["tom-id"] and record["qty-free"] > 0:
            stock_count += 1
            product_id = record["tom-id"]
            with open(file, "a+") as stock_list_file:
                stock_list_file.write(f"{product_id}\n")
    
    if (stock_count == 0):
        print(f"Found no items in stock at {url}! Exiting...")
        sys.exit()
