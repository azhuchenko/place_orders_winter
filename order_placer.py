import json
import requests
import ast
import time
from generate_template import generate_template
from get_stock import get_stock
from get_scs import get_contracts_list
from config import default_stock_filename, default_template_filename, get_token


def place_order(env, location_id, lines_qty, stock_file, template_file):
    get_stock(env, stock_file)
    contracts_list = get_contracts_list(env=env, location_id=location_id)
    service_contract = next(contracts_list)[0:-1]

    order = generate_template(
        env=env,
        location_id=location_id,
        contract=service_contract,
        template_file=template_file, 
        stock_file=stock_file, 
        lines_qty=lines_qty
    )

    endpoint = f"https://co-winter-{env}.tom.takeoff.com/order"
    send_order = requests.post(
        url=endpoint, 
        json=order, 
        headers={
            "X-Token": get_token(env)
        })
    if send_order.status_code != 200:
        response_content = send_order.content
        response_content_dict = ast.literal_eval(response_content.decode("utf-8"))
        if "details-from-3dparty-service" in response_content_dict:
            print(response_content_dict['details-from-3dparty-service']["message"])
        print(f"error sending order {send_order.status_code}")
    else:
        order_id = order["order-id"]
        print(f"{order_id} successfully placed!")
        print("waiting for split")
        time.sleep(1)
        print(f"trying to split {order_id}")
        split_order(env=env, order_id=order_id)
        return order_id
    
    return None


def split_order(env, order_id):
    url = f"https://co-winter-{env}.tom.takeoff.com/order/split/{order_id}"
    split = requests.put(
        url=url, 
        headers={
            "X-Token": get_token(env)
        })
    if split.status_code != 200:
        response_content = split.content
        response_content_dict = ast.literal_eval(response_content.decode("utf-8"))
        print(f"split failed {split.status_code}")
    else:
        print("order split!")

def main():
    # amend qty to specify how many orders you need
    qty = int(input("How many orders do you want? "))

    # select how many lines you want in each order:
    lines_qty = int(input("How many products do you want in each order? "))

    # get env in order to build URLs
    env = input("Which environment do you want to use (delta/s2/uat)? ")
    location_id = input("Which store do you want to use? ")

    stock_file = default_stock_filename()
    template_file = default_template_filename()
    if (input("Do you wish to override additional settings? ").upper() == "Y"):
        stock_file = input("Specify stock file: ")
        template_file = input("Specify template file: ")

    orders_placed = []

    for i in range(qty):
        new_order_id = place_order(
            env=env, 
            location_id=location_id, 
            lines_qty=lines_qty,
            stock_file=stock_file,
            template_file=template_file)
        if (new_order_id != None):
            orders_placed.append(new_order_id)

if __name__ == "__main__":
    main()
