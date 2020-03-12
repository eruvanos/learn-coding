import pytest

from tests.local_dynamo import LocalDynamoDB


@pytest.fixture(scope='session', autouse=True)
def dynamo_db() -> LocalDynamoDB:
    db = LocalDynamoDB()
    db.start()
    print('started dynamo')
    yield db
    print('stopping dynamo')
    db.stop()


@pytest.fixture()
def dynamo_table(dynamo_db) -> 'Table':
    resource = dynamo_db.resource()
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
