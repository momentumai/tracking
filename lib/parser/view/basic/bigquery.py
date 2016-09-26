from urllib import quote
from lib.util.time import to_five_minutes


def get_session_data(data):
    result = {}

    for key in data.iterkeys():
        result['new_' + key] = bool(data[key])

    return result


def get_referrer(context):
    if not context.get('is_share', False):
        return ''

    result = context.get('referrer', '')

    return 'private' if result == '' else result


def get_traffic_type(context):
    if not context.get('is_share', ''):
        return 0

    if context.get('is_paid', ''):
        return 3

    if context.get('is_team', ''):
        return 2

    return 1


def get_campaign(context):
    if not context.get('is_share', False):
        return 0

    campaign = context.get('custom_params', {})

    return int(campaign.get('campaign', 0))


def get_experiment(context):
    if not context.get('is_share', False):
        return 0

    exp = context.get('custom_params', {})

    return exp.get('experiment', '')


def get_campaign_token(context):
    if not context.get('is_share', False):
        return 0

    campaign = context.get('campaign', {})

    return campaign.get('token', '')


def parse(context):
    result = {
        'now': int(to_five_minutes(context['now'])),
        'team_id': int(context['team_id']),
        'content_id': str(context['content']['content_id']),
        'referrer': str(get_referrer(context))[:255],
        'cat1': str(context.get('META_cat1', 'NONE')),
        'cat2': str(context.get('META_cat2', 'NONE')),
        'cat3': str(context.get('META_cat3', 'NONE')),
        'is_share': bool(context.get('is_share', False)),
        'traffic_type': int(get_traffic_type(context)),
        'campaign': int(get_campaign(context)),
        'experiment': str(get_experiment(context))
    }

    result.update(get_session_data(context.get('session_new_on', {})))

    return result
