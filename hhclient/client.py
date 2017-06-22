import requests
import json
import logging

logger = logging.getLogger(__name__)

from . import base
from . import http_client

from . import users


class Client:
    def __init__(self,
                 name=None,
                 password=None,
                 host='127.0.0.1',
                 port=80,
                 secure_connection=False,
                 token=None,
                 schemas=None):

        self.name = name
        self.password = password
        self.host = host
        self.port = port
        self.secure_connection = secure_connection

        self.http_client = http_client.HTTPClient(name,
                                                  password,
                                                  host,
                                                  port,
                                                  secure_connection,
                                                  token
                                                  )

        self.schemas = schemas
        if not self.schemas:
            self.schemas = self.get_schemas()

        self.users = users.UserManager(self,
                schema=self.schemas.get(users.UserManager.__resource_class__.__resource_name__, None))
   
    def authenticate(self, name=None, password=None):
        if name:
            self.name = name
            self.http_client.name = name
        if password:
            self.password = password
            self.http_client.password = password

        data=dict(
            auth=dict(
                identity=dict(
                    methods=['password'],
                    password=dict(
                        user=dict(
                            name=self.name,
                            password=self.password
                        )
                    )
                )
            )
        )

        response, errors= self.http_client.post('/auth', data=data)

        resource = base.Resource(**response)
        return resource

    def get_schemas(self):
        response, status_code = self.http_client.get('/schemas')
        return response
