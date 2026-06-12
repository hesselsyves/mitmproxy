from mitmproxy import http
import json
import os
dir_path = os.path.dirname(os.path.abspath(__file__))
MOCK_RESPONSES = {
    "https://t-api.acerta.be/stratencomponent/address/cities": json.load(
        open(os.path.join(dir_path, "cities_data.json"))
    ),
    "https://t-api.acerta.be/stratencomponent/address/street/search": {
        "streetNames": [
            {"streetName": "Bondgenotenlaan", "streetCode": "12345"}
        ]
    },
}
def request(flow: http.HTTPFlow):
    for url_prefix, data in MOCK_RESPONSES.items():
        if flow.request.pretty_url.startswith(url_prefix):
            flow.response = http.Response.make(
                200, json.dumps(data).encode("utf-8"), {"Content-Type": "application/json"}
            )
            return
