#! /usr/bin/env python3

from requests_pkcs12 import get, post
import os
import json

# For more APIs, please refer to the stacks swagger documentation.

client_store_path = os.getenv('CLIENT_STORE_PATH')
client_store_password = os.getenv('CLIENT_STORE_PASSWORD')
api_heartbeat_url = os.getenv('API_HEARTBEAT_URL')

api_heartbeat_url = api_heartbeat_url + "/heartbeat"
response = get(api_heartbeat_url, verify=False, pkcs12_filename=client_store_path, pkcs12_password=client_store_password)

print(response.text)