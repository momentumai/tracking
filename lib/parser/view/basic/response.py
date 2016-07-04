from lib.util.crypto import encrypt


def parse(visitor_future, cat_future, config, context):
    result = dict()

    visitor = visitor_future.get_result()
    cat_future.get_result()

    visitor_id = visitor.id()
    result['visitor_cookie'] = encrypt(visitor_id, config['encryption_key_visitor'])

    if bool(config.get('debug', False)):
        result['debug'] = {
            'visitor_id': visitor_id,
            'context': context,
            'config': config
        }

    return result
