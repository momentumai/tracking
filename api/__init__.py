from lib.helper.response.xhr import get_error_header


def warmup(environ, start_response):
    response_body = 'Success'
    status = '200'
    response_headers = get_error_header()

    start_response(status, response_headers)

    return [response_body]