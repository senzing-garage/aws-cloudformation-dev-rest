#! /usr/bin/env python3

'''
Example Web application.
'''

# Import from standard library. https://docs.python.org/3/library/

import os
import json

# Import from https://pypi.org/

from flask import Flask, Response
from requests_pkcs12 import get, post

APP = Flask(__name__)

# For more APIs, please refer to this swagger documentation
# https://editor.swagger.io/?url=https://raw.githubusercontent.com/Senzing/senzing-rest-api/master/senzing-rest-api.yaml


@APP.route("/")
def senzing_example_1():
    ''' The root URI. '''

    # Get parameters from environment.

    client_store_p12_file = os.getenv('CLIENT_STORE_P12_FILE')
    secret_client_keystore_password_value = os.getenv('SECRET_CLIENT_KEYSTORE_PASSWORD_VALUE')
    senzing_api_server_url = os.getenv('SENZING_API_SERVER_URL')

    # HTTP request.

    api_heartbeat_url = senzing_api_server_url + "/heartbeat"
    response = get(api_heartbeat_url, verify=False, pkcs12_filename=client_store_p12_file, pkcs12_password=secret_client_keystore_password_value)

    # Return response.

    return Response(response.text, mimetype='application/json')


@APP.route("/test-query")
def senzing_example_2():
    ''' The /test-query URI. '''

    # Get parameters from environment.

    client_store_p12_file = os.getenv('CLIENT_STORE_P12_FILE')
    secret_client_keystore_password_value = os.getenv('SECRET_CLIENT_KEYSTORE_PASSWORD_VALUE')
    senzing_api_server_url = os.getenv('SENZING_API_SERVER_URL')

    # HTTP request.
    # This sample query for jane smith should return nothing as jane smith does not exist.

    api_search_url = senzing_api_server_url + "/search-entities?featureMode=WITH_DUPLICATES&withFeatureStats=false&withInternalFeatures=false&forceMinimal=false&withRelationships=false&withRaw=false"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "accept": "application/json; charset=UTF-8"
    }
    query = {
        "NAME_FIRST": "JANE",
        "NAME_LAST": "SMITH",
        "ADDR_FULL": "123 Main St, Las Vegas NV"
    }
    response = post(api_search_url, verify=False, pkcs12_filename=client_store_p12_file, pkcs12_password=secret_client_keystore_password_value, data=json.dumps(query), headers=headers)

    # Return response.

    return Response(response.text, mimetype='application/json')

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    APP.run()
