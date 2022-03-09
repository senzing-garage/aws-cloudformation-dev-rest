from flask import Flask
from requests_pkcs12 import get, post
import os

app = Flask(__name__)

@app.route("/")
def senzing_example():
    client_store_path = os.getenv('CLIENT_STORE_PATH')
    client_store_password = os.getenv('CLIENT_STORE_PASSWORD')
    api_url = os.getenv('API_URL')

    # heartbeat query
    api_heartbeat_url = api_url + "heartbeat"
    r1 = get(api_heartbeat_url, verify=False, pkcs12_filename=client_store_path, pkcs12_password=client_store_password)
    print(r1.text)

    # sample query for jane smith
    # the query should return nothing as jane smith does not exist
    api_search_url = api_url+ "search-entities?featureMode=WITH_DUPLICATES&withFeatureStats=false&withInternalFeatures=false&forceMinimal=false&withRelationships=false&withRaw=false"
    query = '{ "NAME_FIRST": "JANE", "NAME_LAST": "SMITH", "ADDR_FULL": "123 Main St, Las Vegas NV" }'
    headers = { "Content-Type": "application/json; charset=UTF-8", "accept": "application/json; charset=UTF-8" }
    r2 = post(api_search_url, verify=False, pkcs12_filename=client_store_path, pkcs12_password=client_store_password, data=query, headers=headers)     
    print(r2.text)

    return "ok"