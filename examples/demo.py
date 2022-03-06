from flask import Flask
from requests_pkcs12 import get
import os

app = Flask(__name__)

@app.route("/")
def senzing_heartbeat():
    # heartbeat query
    r = get(os.getenv('API_HEARTBEAT_URL'), verify=False, pkcs12_filename='/Users/chiahuimah/test/my-client-store.p12', pkcs12_password='change-it')
    print(r.text)

    # sample query for jane smith
    query = { "NAME_FIRST": "JANE", "NAME_LAST": "SMITH", "ADDR_FULL": "123 Main St, Las Vegas NV" }
    headers = { "Content-Type": "application/json; charset=UTF-8", "accept": "application/json; charset=UTF-8" }
    r = get(os.getenv('API_SEARCH_URL'), verify=False, pkcs12_filename='/Users/chiahuimah/test/my-client-store.p12', pkcs12_password='change-it', json=query)     
    print(r.text)
    return r.status_code