import requests
import json

mfc_code = "2501"
tgim_stock_endpoint = f"http://10.2.4.213:8090/api/stock/details?mfc-code={mfc_code}"


def get_stock(endpoint=tgim_stock_endpoint):
    with open("stock_list.txt", "r+") as stock:
        stock.truncate(0)
    data = (requests.get(url=tgim_stock_endpoint)).json()
    for record in data:
        if record["tom-id"] and record["qty-free"] > 0:
            product_id = record["tom-id"]
            with open("stock_list.txt", "a+") as stock_list_file:
                stock_list_file.write(f"{product_id}\n")
