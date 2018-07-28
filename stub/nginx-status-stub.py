#!/usr/bin/env python
"""
    NGINX Status Stub
    Returns sample resources usage
"""
from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route("/")
def index():
    response = '''Active connections: 4
server accepts handled requests
1650 1650 9255
Reading: 0 Writing: 1 Waiting: 3'''
    return response, 200


@app.route("/nginx_status", strict_slashes=False)
def nginx_status():
    response = '''Active connections: 4
server accepts handled requests
1650 1650 9255
Reading: 0 Writing: 1 Waiting: 3'''
    return response, 200
