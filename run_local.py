from contextlib import contextmanager

import log_util
from app import create_app
from tests.local_dynamo import LocalDynamoDB


@contextmanager
def dynamo_table(resource) -> 'Table':
    resource.create_table(
        TableName='test_table',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'version',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'version',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        })

    table = resource.Table('test_table')
    yield table
    table.delete()


if __name__ == '__main__':
    log_util.configure(log_format=log_util.NO_TIME_FORMAT)

    with LocalDynamoDB() as db:
        with dynamo_table(db) as table:
            app = create_app(table)
            app.debug = True
            app.run('127.0.0.1', debug=True)