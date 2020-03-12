import os
import shutil
import tarfile
from uuid import uuid4

import boto3
import mirakuru
import requests
from mirakuru import TCPExecutor

LATEST_URL = 'https://s3.eu-central-1.amazonaws.com/dynamodb-local-frankfurt/dynamodb_local_latest.tar.gz'


class LocalDynamoDB:
    def __init__(self, path='/tmp/dynamodb'):
        self._path = path
        self._path_dynamodb_jar = os.path.join(path, 'DynamoDBLocal.jar')

        self._port = self._get_open_port()
        self.executor = TCPExecutor(
            f'java -Djava.library.path=./DynamoDBLocal_lib -jar {self._path_dynamodb_jar} -inMemory -port {self._port}',
            host='localhost',
            port=self._port,
            timeout=60,
        )

        # Write random credentials into env
        self.aws_access_key = str(uuid4())
        self.aws_secret_access_key = str(uuid4())
        self.region = str(uuid4())

        os.environ['AWS_ACCESS_KEY_ID'] = self.aws_access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = self.aws_secret_access_key
        os.environ['AWS_DEFAULT_REGION'] = self.region

        self.__resources = set()

    def start(self):
        self._ensure_dynamodb_local()
        self.executor.start()
        return self

    def __enter__(self):
        self.start()
        return self.resource()

    def clear(self):
        for t in self.resource().tables.all():
            t.delete()

    def stop(self):
        # for resource in self.__resources:
        #     resource.
        try:
            self.executor.stop()
        except mirakuru.exceptions.ProcessFinishedWithError:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def resource(self):
        dynamo_db = boto3.resource(
            'dynamodb',
            endpoint_url=f'http://localhost:{self._port}'
        )

        self.__resources.add(dynamo_db)
        return dynamo_db

    def credentials(self, table='table'):
        return {
            'access_key': self.aws_access_key,
            'region': self.region,
            'secret_access_key': self.aws_secret_access_key,
            'table': table,
            'endpoint_url': f'http://localhost:{self._port}'
        }

    @staticmethod
    def _get_open_port():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port

    def _ensure_dynamodb_local(self):
        if os.path.exists(self._path_dynamodb_jar):
            print(f'Use existing DynamoDB setup in "{self._path}"')

        else:
            print(f'Download dynamodb jar to "{self._path}"')
            self._download_dynamodb()

    def _download_dynamodb(self):
        print(f'Download dynamodb local to "{self._path}"')

        if os.path.exists(self._path):
            print(f'Clean "{self._path}"')
            shutil.rmtree(self._path)

        with requests.get(LATEST_URL, stream=True) as r:
            r.raise_for_status()

            with tarfile.open(fileobj=r.raw, mode='r:gz') as tar:
                tar.extractall(self._path)

        for p in os.listdir(self._path):
            print(p)