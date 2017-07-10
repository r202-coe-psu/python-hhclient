import requests
import json
import logging

logger = logging.getLogger(__name__)

from . import base
from . import http_client

# from . import users


class Client:
    def __init__(self,
                 api_url,
                 access_token,
                 schemas=None):

        self.api_url = api_url
        self.access_token = access_token

        self.http_client = http_client.HTTPClient(
                access_token
                )

        self.schemas = schemas
        if not self.schemas:
            self.schemas = self.get_schemas()

        
        retrieve_schema = lambda m:\
            self.schemas.get(m.__resource_class__.__resource_name__,
                             None)
        # self.users = users.UserManager(self,
        #         schema=retrieve_schema(users.UserManager))

    def get_schemas(self):
        response, status_code = self.http_client.get('/schemas')
        return response
