from hhclient.common import client

from . import inventories

import logging

logger = logging.getLogger(__name__)


class Client(client.BaseClient):
    def __init__(self,
                 api_url,
                 access_token,
                 schemas=None):

        super().__init__(api_url, access_token, schemas)

        self.inventories = inventories.InventoryManager(
                self,
                schema=self.retrieve_schema(
                    inventories.InventoryManager))
