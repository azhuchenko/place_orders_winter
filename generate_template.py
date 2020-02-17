import json
import random
import sys
from get_scs import get_scs

def add_lineitems(stock_file, template_file, qty):
    with open(template_file, "r+") as templ:
        templ = json.loads(templ.read())
        data = (open(stock_file, "r+")).read()
        if data:
            item_list = random.choices(data.split("\n"), k=qty)
            line_id = 0
            templ["line-items"] = []
            for item in item_list:
                if item.strip():
                    requested_count = random.randint(1, 4)
                    line_id += 1
                    templ["line-items"].append(
                        {'takeoff-item-ids': [item],
                        'ecom-item-id': item,
                        'requested-quantity': requested_count,
                        'ecom-line-id': str("line_id")
                        })
        else:
            return "OOS"
        with open(template_file, "w+") as template:
            template.write(json.dumps(templ))


def add_service_contract(env, location_id, contract, file):
    get_scs(env=env, location_id=location_id)
    with open(file, "r+") as templ:
        templ = json.loads(templ.read())
        templ["fulfillment-datetime"] = contract
        with open(file, "w+") as template:
            template.write(json.dumps(templ))


def set_order_id(file):
    order_id = f"test{random.randint(0, 999999)}"
    with open(file, "r+") as templ:
        templ = json.loads(templ.read())
        templ["order-id"] = order_id
        templ["ecom-order-id"] = order_id
        with open(file, "w+") as template:
            template.write(json.dumps(templ))
    return order_id


def generate_template(env,
                      location_id,
                      template_file, 
                      stock_file, 
                      contract,
                      lines_qty=1):
    add_service_contract(
        env=env, 
        location_id=location_id, 
        contract=contract,
        file=template_file)
    if add_lineitems(
        stock_file=stock_file,
        template_file=template_file,
        qty=lines_qty
    ) == "OOS":
        print("OOS")
        sys.exit()
    set_order_id(file=template_file)
    order = json.loads(open(template_file).read())
    return order
