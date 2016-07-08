from datetime import datetime
from googleapiclient.discovery import build
from oauth2client.contrib.appengine import AppAssertionCredentials
import httplib2
import uuid
import logging


credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/bigquery')
service = build('bigquery', 'v2')


def stream_row(data, config):
    request_id = str(uuid.uuid4())
    insert_all_data = {
        'templateSuffix': datetime.fromtimestamp(data['now']).strftime('_%Y%m%d%H'),
        'rows': [{
            'json': {
                'id': request_id,
                'time': data['now'],
                'team_id': data['team_id'],
                'cat1': data['cat1'],
                'cat2': data['cat2'],
                'cat3': data['cat3'],
                'content_id': data['content_id'],
                'category_map': data.get('category_map', ''),
                'referrer': data['referrer'],
                'is_share': data['is_share'],
                'traffic_type': data['traffic_type'],
                'campaign': data['campaign'],
                'new_content': data.get('new_content', False),
                'new_cat0': data.get('new_cat0', False),
                'new_cat1': data.get('new_cat1', False),
                'new_cat2': data.get('new_cat2', False),
                'new_cat3': data.get('new_cat3', False)
            },
            'insertId': request_id,
        }]
    }
    logging.info('Send to BigQuery')
    logging.info(insert_all_data)
    http = credentials.authorize(httplib2.Http())
    response = service.tabledata().insertAll(
        projectId=config['project_id'],
        datasetId=config['env'] + '_realtime',
        tableId='views',
        body=insert_all_data
    ).execute(http=http, num_retries=3)

    logging.info('bigquery response:')
    logging.info(response)

    return response
