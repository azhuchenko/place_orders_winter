import json
import requests
import ast
from generate_template import add_lineitems, add_service_contract, set_order_id
from get_stock import get_stock
from get_scs import get_scs
import sys
import time

# amend qty to specify how many orders you need

qty = 30
how_many_orders = list(range(1, qty+1))

# select how many lines you want in each order:

lines_qty = 30

# set endpoint - suitable for OMS only

endpoint = "https://co-winter-delta.tom.takeoff.com/order"
split_endpoint = "https://co-winter-delta.tom.takeoff.com/order/split/"

# read list of contracts from file and add them to list for usage

get_scs()
contracts_list = open("contracts_list.txt", "r")

order = json.loads(open("order_template.json").read())

orders_placed = []


def place_orders():
    get_stock()
    service_contract = next(contracts_list)[0:-1]
    add_service_contract(service_contract)
    if add_lineitems("stock_list.txt", lines_qty) == "OOS":
        print("OOS")
        sys.exit()
    set_order_id()
    order = json.loads(open("order_template.json").read())
    send_order = requests.post(url=endpoint, json=order, headers={
        "X-Token": "zd5PeCgkhSqWyPaYw7WNQuqs"})
    if send_order.status_code != 200:
        response_content = send_order.content
        response_content_dict = ast.literal_eval(response_content.decode("utf-8"))
        if "details-from-3dparty-service" in response_content_dict:
            print(response_content_dict['details-from-3dparty-service']["message"])
        print(f"error sending order {send_order.status_code}")
    else:
        successful_order = order["order-id"]
        orders_placed.append(successful_order)
        print(f"{successful_order} successfully placed!")
        print("waiting for split")
        time.sleep(1)
        print(f"trying to split {successful_order}")
        split_orders(successful_order)
    return orders_placed


def split_orders(placed_order):
    url = f"{split_endpoint + placed_order}"
    split = requests.put(url=url, headers={"X-Token": "zd5PeCgkhSqWyPaYw7WNQuqs"})
    if split.status_code != 200:
        response_content = split.content
        response_content_dict = ast.literal_eval(response_content.decode("utf-8"))
        print(f"split failed {split.status_code}")
    else:
        print("order split!")


for i in how_many_orders:
    place_orders()
