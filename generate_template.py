import json
import random
from get_scs import get_scs

contracts_list = open("contracts_list.txt", "r")
service_contract = next(contracts_list)[0:-1]


def add_lineitems(file, qty):
    with open("order_template.json", "r+") as templ:
        templ = json.loads(templ.read())
        data = (open(file, "r+")).read()
        if data:
            item_list = random.choices(data.split("\n"), k=qty)
            line_id = 0
            templ["line-items"] = []
            for item in item_list:
                if item.strip():
                    requested_count = random.randint(5, 10)
                    line_id += 1
                    templ["line-items"].append(
                        {'takeoff-item-ids': [item],
                        'ecom-item-id': item,
                        'requested-quantity': requested_count,
                        'ecom-line-id': str("line_id")
                        })
        else:
            return "OOS"
        with open("order_template.json", "w+") as template:
            template.write(json.dumps(templ))


def add_service_contract(contract):
    get_scs()
    with open("order_template.json", "r+") as templ:
        templ = json.loads(templ.read())
        templ["fulfillment-datetime"] = contract
        with open("order_template.json", "w+") as template:
            template.write(json.dumps(templ))


def set_order_id(file="order_template.json"):
    orders = []
    with open("order_template.json", "r+") as templ:
        templ = json.loads(templ.read())
        order_id = f"delta{random.randint(0, 999999)}"
        orders.append(order_id)
        templ["order-id"] = order_id
        templ["ecom-order-id"] = order_id
        with open("order_template.json", "w+") as template:
            template.write(json.dumps(templ))
    return orders


def generate_template(template_file="order_template.json", stock_file="stock_list.txt", contract=service_contract,
                      qty_of_items_in_order=1):
    add_service_contract(contract)
    add_lineitems(stock_file, qty_of_items_in_order)
    set_order_id(template_file)
