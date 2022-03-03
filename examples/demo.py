from flask import Flask
from requests_pkcs12 import get
import os

app = Flask(__name__)

@app.route("/")
def senzing_heartbeat():
    r = get(os.getenv('API_URL'), verify=False, pkcs12_filename='/Users/chiahuimah/test/my-client-store.p12', pkcs12_password='change-it')
    return r.text