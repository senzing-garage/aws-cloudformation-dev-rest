#! /usr/bin/env python3

from requests_pkcs12 import get, post
import os
import json

# For more APIs, please refer to this swagger documentation
# https://editor.swagger.io/?url=https://raw.githubusercontent.com/Senzing/senzing-rest-api/master/senzing-rest-api.yaml

client_store_path = os.getenv('CLIENT_STORE_PATH')
client_store_password = os.getenv('CLIENT_STORE_PASSWORD')
api_url = os.getenv('API_URL')

api_heartbeat_url = api_url + "/heartbeat"
response = get(api_heartbeat_url, verify=False, pkcs12_filename=client_store_path, pkcs12_password=client_store_password)

print(response.text)