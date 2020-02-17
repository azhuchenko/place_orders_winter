def get_all_config():
    return {
        "s2": {
            "ip": "10.2.4.200",
        },
        "s3": {
            "ip": "10.2.4.210",
        },
        "delta": {
            "ip": "10.2.4.213",
        },
        "uat": {
            "ip": "10.2.4.212",
        }
    }

def get_ip(env):
    all_config = get_all_config()
    return all_config[env]['ip']

def get_token(env):
    return "zd5PeCgkhSqWyPaYw7WNQuqs"

def get_mfc_code(env):
    return "2501"

def default_stock_filename():
    return "stock_list.txt"

def default_template_filename():
    return "order_template.json"