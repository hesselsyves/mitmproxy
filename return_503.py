from mitmproxy import http

TARGET_URL = "https://testt-api.acerta.be/WSConsultKBO/8.0/consultEntity"   # URL die je wilt blokkeren

def request(flow: http.HTTPFlow):
    if flow.request.pretty_url.startswith(TARGET_URL):
        flow.response = http.Response.make(
            503,                       # Status code
            b"Service Unavailable",     # Body
            {"Content-Type": "text/plain"}  # Headers
        )

