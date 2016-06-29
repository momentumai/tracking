import json


def get_error_header():
    return [
        ('Content-Type', 'text/plain'),
        ('Access-Control-Allow-Methods', '*'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Headers', 'Content-Type')
    ]


def start_api_response(response, start_response):
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Methods', '*'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Headers', 'Content-Type')
    ]

    start_response(status, response_headers)

    return [json.dumps(response)]
