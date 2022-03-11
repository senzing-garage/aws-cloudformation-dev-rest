from flask import Flask, Response
from requests_pkcs12 import get, post
import os
import json

app = Flask(__name__)

# For more APIs, please refer to the stacks swagger documentation.

@app.route("/")
def senzing_example_1():

    # Get parameters from environment.

    client_store_path = os.getenv('CLIENT_STORE_PATH')
    client_store_password = os.getenv('CLIENT_STORE_PASSWORD')
    api_heartbeat_url = os.getenv('API_HEARTBEAT_URL')

    # HTTP request.

    api_heartbeat_url = api_heartbeat_url + "/heartbeat"
    response = get(api_heartbeat_url, verify=False, pkcs12_filename=client_store_path, pkcs12_password=client_store_password)

    # Return response.

    return Response(response.text, mimetype='application/json')


@app.route("/test-query")
def senzing_example_2():

    # Get parameters from environment.

    client_store_path = os.getenv('CLIENT_STORE_PATH')
    client_store_password = os.getenv('CLIENT_STORE_PASSWORD')
    api_heartbeat_url = os.getenv('API_HEARTBEAT_URL')

    # HTTP request.
    # This sample query for jane smith should return nothing as jane smith does not exist.

    api_search_url = api_heartbeat_url + "/search-entities?featureMode=WITH_DUPLICATES&withFeatureStats=false&withInternalFeatures=false&forceMinimal=false&withRelationships=false&withRaw=false"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "accept": "application/json; charset=UTF-8"
    }
    query = {
        "NAME_FIRST": "JANE",
        "NAME_LAST": "SMITH",
        "ADDR_FULL": "123 Main St, Las Vegas NV"
    }
    response = post(api_search_url, verify=False, pkcs12_filename=client_store_path, pkcs12_password=client_store_password, data=json.dumps(query), headers=headers)

    # Return response.

    return Response(response.text, mimetype='application/json')

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    app.run()
