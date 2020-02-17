import requests
import zulu
from config import get_token

def get_scs_url(env, location_id):
    return f"https://scs-winter-{env}.tom.takeoff.com/api/service-contracts?location-id={location_id}"

def get_scs(env, location_id):
    with open("contracts_list.txt", "r+") as scs:
        scs.truncate(0)
    url = get_scs_url(env=env, location_id=location_id)
    data = (requests.get(url=url, headers={"X-Token": get_token(env)})).json()
    contracts = []
    for record in data:
        contracts.append(record["service-window-start"])
    for contract in contracts:
        dt = zulu.parse(contract)
        usable_contract = f"{(dt.isoformat())[0:-6]}" + "Z"
        with open("contracts_list.txt", "a+") as contracts_list_file:
            contracts_list_file.write(f"{usable_contract}\n")

def get_contracts_list(env, location_id):
    get_scs(env=env, location_id=location_id)
    contracts_list = open("contracts_list.txt", "r")
    return contracts_list
