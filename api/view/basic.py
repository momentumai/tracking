from config import get_config
from lib.error.validation import ValidationError
from lib.helper.request.params import get_post_params_from_json
from lib.helper.response.xhr import start_api_response
from lib.parser.view.basic import \
    request, visitor, response, kinesis, bigquery, future
from lib.model.content import get_by_url, update_content
from lib.model.category import get_or_insert_async
from google.appengine.api import namespace_manager
from time import time
from lib.resource.kinesis import push_record
from lib.resource import bigquery as bigquery_resource


def put(environ, start_response):
    ret = dict()
    try:
        if environ['REQUEST_METHOD'] == 'POST':
            local = dict()

            config = get_config(environ)
            params = get_post_params_from_json(environ)

            params['now'] = int(time())

            local.update(request.parse(config, params))
            namespace_manager.set_namespace(str(local['team_id']))

            content = get_by_url(local['page'], local)
            content_future = update_content(content, local)
            local['content'] = content.to_dict()

            visitor_obj, visitor_future = visitor.parse(local)
            cat_future = get_or_insert_async(local['category_map'])

            local.update(visitor_obj)
            local['kinesis'] = kinesis.parse(local)
            local['bigquery'] = bigquery.parse(local)

            if not content.is_blacklisted:
                if not local.get('is_in_house', False):
                    local['bigquery_response'] = bigquery_resource.stream_row(
                        local['bigquery'],
                        config
                    )
            visitor_obj = future.get_results(
                visitor_future,
                cat_future,
                content_future
            )
            ret = response.parse(visitor_obj, config, local)

    except ValidationError as err:
        ret['error'] = str(err)

    return start_api_response(ret, start_response)
