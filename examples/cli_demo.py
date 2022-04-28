#! /usr/bin/env python3

'''
Example Command line interface.
'''

# Import from standard library. https://docs.python.org/3/library/

import os

# Import from https://pypi.org/

from requests_pkcs12 import get

# For more APIs, please refer to this swagger documentation
# https://editor.swagger.io/?url=https://raw.githubusercontent.com/Senzing/senzing-rest-api/master/senzing-rest-api.yaml

CLIENT_STORE_P12_FILE = os.getenv('CLIENT_STORE_P12_FILE')
SECRET_CLIENT_KEYSTORE_PASSWORD_VALUE = os.getenv('SECRET_CLIENT_KEYSTORE_PASSWORD_VALUE')
SENZING_API_SERVER_URL = os.getenv('SENZING_API_SERVER_URL')

API_HEARTBEAT_URL = SENZING_API_SERVER_URL + "/heartbeat"
RESPONSE = get(API_HEARTBEAT_URL, verify=False, pkcs12_filename=CLIENT_STORE_P12_FILE, pkcs12_password=SECRET_CLIENT_KEYSTORE_PASSWORD_VALUE)

print(RESPONSE.text)
