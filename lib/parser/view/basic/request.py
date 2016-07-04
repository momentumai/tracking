from lib.error.validation import ValidationError
from lib.model import team
from lib.model import visitor
from lib.parser import url
from base64 import standard_b64encode
from urllib import quote


def validate(context):
    if context['team_id'] == 0:
        raise ValidationError('Couldn\'t find team id')
    if context['page'] == '':
        raise ValidationError('Couldn\'t find valid url')


def decryption(config, params):
    result = dict()

    result['team_id'] = team.decrypt_id(params.get('user_id', ''), config)
    result['visitor_id'] = visitor.decrypt_id(params.get('visitor_id', ''), config)
    result['extension_team'] = team.decrypt_id(params.get('bv_team', ''), config)

    return result


def parse_url(params):
    result = dict()

    result['original_url'] = params.get('page', '')
    result['page'] = result['original_url'][:255]
    result['domain_name'] = url.get_domain_name(result['page'])
    result['custom_params'] = params.get('custom_params', {})

    if params.get('referrer_overwrite', '') == '1':
        result['referrer'] = url.overwrite_by_domain(params.get('referrer', ''))
    else:
        result['referrer'] = url.get_domain_name(params.get('referrer', ''))

    if result['custom_params'].get('source', '') != '':
        result['referrer'] = url.overwrite_by_domain(str(result['custom_params']['source']))

    return result


def parse_meta(context):
    result = dict()

    for key, value in context.items():
        if key in ('author', 'title'):
            result['META_' + key] = standard_b64encode(str(value.encode('utf8')))
        else:
            result['META_' + key] = quote(str(value.encode('utf8')))

    result['META_cat1'] = result['META_cat1'] if result.get('META_cat1', '') != '' else 'NONE'
    result['META_cat2'] = result['META_cat2'] if result.get('META_cat2', '') != '' else 'NONE'
    result['META_cat3'] = result['META_cat3'] if result.get('META_cat3', '') != '' else 'NONE'

    result['category_map'] = '||'.join([
        result['META_cat1'],
        result['META_cat2'],
        result['META_cat3']
    ])

    return result


def is_organic(page_url):
    return page_url.startswith('www.google', 0, 10)


def is_share(context):
    result = dict()

    referrer = context.get('referrer', '')
    referrer = url.get_domain_name(referrer)

    if referrer != context.get('domain_name', 'NONE') and not is_organic(referrer):
        result['is_share'] = True

    return result


def is_in_house(context):
    result = dict()

    if context['team_id'] == context.get('extension_team', False):
        result['is_in_house'] = True

    return result


def is_paid(context):
    result = dict()

    if context['custom_params'].get('p', '') != '' or context.get('is_paid', False):
        result['is_paid'] = True

    return result


def is_team(context):
    result = dict()

    if context['custom_params'].get('t', '') != '':
        result['is_team'] = True

    return result


def parse_share(context):
    result = dict()

    if context['custom_params'].get('campaign', '') != '' and context['custom_params'].get('token', '') != '':
        result['campaign'] = {
            'id': context['custom_params']['campaign'],
            'token': context['custom_params']['token']
        }

    return result


# to be compatible with the previous system
def add_bulk(context):
    return {
        'post_status': '',
        'gen': '1' if context.get('is_share', False) else '0'
    }


def parse(config, params):
    result = dict()

    result['now'] = params['now']

    result.update(decryption(config, params))
    result.update(parse_url(params))
    result.update(parse_meta(params.get('meta', dict())))

    validate(result)

    result.update(is_paid(result))
    result.update(is_team(result))
    result.update(is_share(result))
    result.update(is_in_house(result))

    if result.get('is_share', False):
        result.update(parse_share(result))

    result.update(add_bulk(result))

    return result
