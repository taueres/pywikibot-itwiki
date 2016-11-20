# -*- coding: utf-8 -*-
"""Module for network common functions"""

import requests

def fetch_url_resource(url):
    req = requests.get(url)
    return req.text
