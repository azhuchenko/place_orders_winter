import requests
import zulu

location_id = "WF0134"
request_url = f"https://scs-winter-delta.tom.takeoff.com/api/service-contracts?location-id="


def get_scs(endpoint=request_url, location=location_id):
    with open("contracts_list.txt", "r+") as scs:
        scs.truncate(0)
    url = endpoint+location
    data = (requests.get(url=url, headers={"X-Token": "zd5PeCgkhSqWyPaYw7WNQuqs"})).json()
    contracts = []
    for record in data:
        contracts.append(record["service-window-start"])
    for contract in contracts:
        dt = zulu.parse(contract)
        usable_contract = f"{(dt.isoformat())[0:-6]}" + "Z"
        with open("contracts_list.txt", "a+") as contracts_list_file:
            contracts_list_file.write(f"{usable_contract}\n")


get_scs()
pass
