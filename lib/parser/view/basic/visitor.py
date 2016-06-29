from lib.model.visitor import get_by_id


def update_visitor(visitor, context):
    result = {
        'content': 0,
        'cat0': 0,
        'cat1': 0,
        'cat2': 0,
        'cat3': 0
    }

    if context['page'] not in visitor.session.visited_contents:
        visitor.session.visited_contents.append(context['page'])
        result['content'] = 1

    if visitor.session.is_new:
        result['cat0'] = 1

    if context['META_cat1'] not in visitor.session.visited_cat1_contents:
        visitor.session.visited_cat1_contents.append(context['META_cat1'])
        result['cat1'] = 1

    if context['META_cat2'] not in visitor.session.visited_cat2_contents:
        visitor.session.visited_cat2_contents.append(context['META_cat2'])
        result['cat2'] = 1

    if context['META_cat3'] not in visitor.session.visited_cat3_contents:
        visitor.session.visited_cat3_contents.append(context['META_cat3'])
        result['cat3'] = 1

    return result


def parse(context):
    result = dict()

    visitor = get_by_id(context['visitor_id'])

    result['session_new_on'] = update_visitor(visitor, context)

    visitor_future = visitor.put_async()

    return result, visitor_future
