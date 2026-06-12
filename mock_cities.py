from mitmproxy import http
import json
import os

TARGET_URL = "https://t-api.acerta.be/stratencomponent/address/cities"


def request(flow: http.HTTPFlow):
    if flow.request.pretty_url.startswith(TARGET_URL):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dir_path, "cities_data.json")) as f:
            data = json.load(f)
        flow.response = http.Response.make(
            200, json.dumps(data).encode("utf-8"), {"Content-Type": "application/json"}
        )
