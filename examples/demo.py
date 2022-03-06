from flask import Flask
from requests_pkcs12 import get
import os

app = Flask(__name__)

@app.route("/")
def senzing_example():
    client_store_path = os.getenv('CLIENT_STORE_PATH')
    client_store_password = os.getenv('CLIENT_STORE_PASSWORD')
    api_heartbeat_url = os.getenv('API_HEARTBEAT_URL')
    api_search_url = os.getenv('API_SEARCH_URL')

    # heartbeat query
    r1 = get(api_heartbeat_url, verify=False, pkcs12_filename=client_store_path, pkcs12_password=client_store_password)
    print(r1.text)

    # sample query for jane smith
    query = { "NAME_FIRST": "JANE", "NAME_LAST": "SMITH", "ADDR_FULL": "123 Main St, Las Vegas NV" }
    headers = { "Content-Type": "application/json; charset=UTF-8", "accept": "application/json; charset=UTF-8" }
    r2 = get(api_search_url, verify=False, pkcs12_filename=client_store_path, pkcs12_password=client_store_password, json=query)     
    print(r2.text)
    return (r1.status_code, r2.status_code)