from urlparse import urlparse, parse_qs


def get_domain_name(url):
    parsed = urlparse(url)
    parsed = 'http://' + parsed.netloc + parsed.path
    parsed = urlparse(parsed)

    return parsed.netloc


def overwrite_by_domain(text):
    url_map = {
        'facebook': 'facebook.com',
        'twitter': 't.co'
    }

    text = str(text).lower()
    domain = url_map.get(text, '')

    return text if domain == '' else domain
