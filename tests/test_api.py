from uuid import uuid4

import pytest
from boto3.dynamodb.conditions import Key
from flask import Response
from flask.testing import FlaskClient

from app import create_app


@pytest.fixture()
def client(dynamo_table) -> FlaskClient:
    app = create_app(dynamo_table)
    # app.debug = True

    with app.test_client() as client:
        yield client


def test_ping(client, dynamo_table):
    response: Response = client.get('/ping')

    assert response.status_code == 200, response.data
    assert response.data.decode() == 'pong'


def test_get_all_teams(client, dynamo_table):
    # GIVEN
    dynamo_table.put_item(
        Item={
            'id': 'hubble',
            'version': '1'
        }
    )

    # WHEN
    response: Response = client.get('/api/teams')

    # THEN
    assert response.status_code == 200, response.data.decode()
    teams = response.json
    assert teams == [{'id': 'hubble', 'version': '1'}]


def test_get_existing_team(client, dynamo_table):
    # GIVEN
    team_name = str(uuid4())
    dynamo_table.put_item(
        Item={
            'id': team_name,
            'version': '1'
        }
    )

    # WHEN
    response: Response = client.get(f'/api/teams/{team_name}')

    # THEN
    assert response.status_code == 200, response.data.decode()
    assert response.json == {'id': team_name, 'version': '1'}


def test_get_none_existing_team(client, dynamo_table):
    # GIVEN
    team_name = str(uuid4())

    # WHEN
    response: Response = client.get(f'/api/teams/{team_name}')

    # THEN
    assert response.status_code == 404, response.data.decode()


def test_create_team(client, dynamo_table):
    # GIVEN
    team_name = str(uuid4())

    # WHEN
    response: Response = client.put(f'/api/teams',
                                    json={
                                        'id': team_name,
                                        'version': '1'
                                    })

    # THEN
    assert response.status_code == 201, response.data.decode()

    actual_team = dynamo_table.get_item(Key={'id': team_name, 'version': '1'}).get('Item')
    assert actual_team == {'id': team_name, 'version': '1'}


def test_save_code(client, dynamo_table):
    # GIVEN
    team_name = str(uuid4())

    # WHEN
    response: Response = client.put(f'/api/teams',
                                    json={
                                        'id': team_name,
                                        'version': '1',
                                        'code': 'print("hello world")'
                                    })

    # THEN
    assert response.status_code == 201, response.data.decode()

    actual_team = dynamo_table.get_item(Key={'id': team_name, 'version': '1'}).get('Item')
    assert actual_team == {'id': team_name, 'version': '1', 'code': 'print("hello world")'}


def test_save_code_as_new_version(client, dynamo_table):
    team_name = str(uuid4())
    dynamo_table.put_item(
        Item={
            'id': team_name,
            'version': '1',
        }
    )

    response: Response = client.post(f'/api/teams/{team_name}',
                                     json={
                                         'id': team_name,
                                         'code': 'print("hello world")'
                                     })

    assert response.status_code == 200, response.data.decode()

    all_versions = dynamo_table.query(
        KeyConditionExpression=Key('id').eq(team_name),
        ScanIndexForward=False
    ).get('Items', [])
    assert len(all_versions) == 2

    latest_version = all_versions[0]
    assert latest_version['code'] == 'print("hello world")'


def test_get_team_returns_newest_version(client, dynamo_table):
    team_name = str(uuid4())
    dynamo_table.put_item(
        Item={
            'id': team_name,
            'version': '2020-04-07T12:00:00.000000'
        }
    )
    dynamo_table.put_item(
        Item={
            'id': team_name,
            'version': '2020-04-07T12:05:00.000000'
        }
    )

    response: Response = client.get(f'/api/teams/{team_name}')

    assert response.status_code == 200, response.data.decode()

    assert response.json == {'id': team_name, 'version': '2020-04-07T12:05:00.000000'}

