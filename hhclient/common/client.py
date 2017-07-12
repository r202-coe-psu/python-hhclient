from . import http_client

import logging

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self,
                 api_url,
                 access_token,
                 schemas=None):

        self.api_url = api_url
        self.access_token = access_token
        self.schemas = schemas

        self.http_client = http_client.HTTPClient(
                api_url,
                access_token
                )

        self.schemas = schemas
        if not self.schemas:
            self.schemas = self.get_schemas()

    def retrieve_schema(self, manager):
        return self.schemas.get(
                manager.__resource_class__.__resource_name__,
                None)

    def get_schemas(self):
        response, status_code = self.http_client.get('/schemas')
        return response
