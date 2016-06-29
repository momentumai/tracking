from urllib import quote
from lib.util.time import to_five_minutes


def get_referrer(context):
    if not context.get('is_share', False):
        return ''

    result = context.get('referrer', '')

    return 'private' if result == '' else result


def get_traffic_type(context):
    if not context.get('is_share', False):
        return False

    if context.get('is_paid', False) or bool(get_campaign(context)):
        return 'paid'

    if context.get('is_team', False):
        return 'team'

    return 'organic'


def get_campaign(context):
    if not context.get('is_share', False):
        return 0

    campaign = context.get('custom_params', {})

    return int(campaign.get('campaign', 0))


def get_campaign_token(context):
    if not context.get('is_share', False):
        return 0

    campaign = context.get('custom_params', {})

    return campaign.get('t', '')


def parse(context):
    return {
        'type': 'pageview',
        'now': to_five_minutes(context['now']),
        'team_id': int(context['team_id']),
        'url': quote(context.get('page', '')),
        'referrer': get_referrer(context),
        'cat1': context.get('META_cat1', 'NONE'),
        'cat2': context.get('META_cat2', 'NONE'),
        'cat3': context.get('META_cat3', 'NONE'),
        'title': context.get('META_title', ''),
        'image': context.get('META_image_url', ''),
        'is_share': context.get('is_share', False),
        'gen': int(context.get('gen', 0)),
        'traffic_type': get_traffic_type(context),
        'session_new': context.get('session_new_on', {}),
        'campaign': get_campaign(context),
        'token': get_campaign_token(context)
    }
