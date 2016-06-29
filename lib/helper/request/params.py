import json


def get_post_params_from_json(environ):
    params = '{}'
    try:
        length = int(environ.get('CONTENT_LENGTH', '0'))
    except ValueError:
        length = 0
    if length != 0:
        params = environ['wsgi.input'].read(length)
    try:
        return json.loads(params)
    except ValueError:
        return {}
