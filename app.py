# ServeR
import logging
import os

import boto3
import cfenv
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cachebuster import CacheBuster
from flaskext.markdown import Markdown

import log_util
from log_util import log_error

logger = logging.getLogger('api')


def get_table_from_vcap(service_name) -> 'Table':
    app_env = cfenv.AppEnv()

    db = app_env.get_service(name=service_name)
    if db is None:
        raise Exception(f'Requires service \'{service_name}\'')

    creds = db.credentials
    resource = boto3.resource('dynamodb',
                              aws_access_key_id=creds['access_key'],
                              aws_secret_access_key=creds['secret_access_key'],
                              region_name=creds['region'],
                              endpoint_url=creds.get('endpoint'),
                              )
    return resource.Table(creds['table'])


def create_app(table: 'Table') -> Flask:
    app = Flask(__name__)
    app.logger = logger.getChild('flask')

    Markdown(app, extensions=['codehilite', 'fenced_code'])

    config = {'extensions': ['.css'], 'hash_size': 5}
    cache_buster = CacheBuster(config=config)
    cache_buster.init_app(app)

    # Version
    DEFAULT_VERSION = '1'

    # Health
    @app.route('/ping')
    @log_error
    def index():
        return 'pong'

    # API
    @app.route('/api/teams')
    @log_error
    def teams():
        return jsonify(table.scan()['Items']), 200

    @app.route('/api/teams/<team_name>')
    @log_error
    def get_team(team_name):
        item = table.get_item(Key={'id': team_name, 'version': DEFAULT_VERSION}).get('Item')
        if item is None:
            return 'No team found.', 404
        else:
            return jsonify(item), 200

    @app.route('/api/teams', methods=['PUT'])
    @log_error
    def put_item():
        team = request.get_json(silent=True)
        team['version'] = DEFAULT_VERSION
        table.put_item(
            Item=team
        )
        return '', 201

    @app.route('/api/teams/<team_name>', methods=['POST'])
    @log_error
    def update_item(team_name):
        team = request.get_json(silent=True)
        team['id'] = team_name
        team['version'] = DEFAULT_VERSION

        # Update version instead
        table.put_item(
            Item=team
        )
        return '', 200

    # UI
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/x-icon')

    @app.route('/')
    def choose_team():
        return render_template('chooseTeam.html')

    @app.route('/teams/<team_name>')
    def editor(team_name):
        with app.open_resource('docs/learn-coding.md', 'rt') as f:
            content = f.read()

        return render_template('editor.html', team_name=team_name, tutorial_text=content)

    return app


if __name__ == '__main__':
    log_util.configure(log_format=log_util.NO_TIME_FORMAT)

    table = get_table_from_vcap('learn-coding-db')
    app = create_app(table)

    app.run('0.0.0.0', port=cfenv.AppEnv().port)
