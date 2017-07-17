from hhclient.common import client

from . import stocks
from . import items

import logging

logger = logging.getLogger(__name__)


class Client(client.BaseClient):
    def __init__(self,
                 api_url,
                 access_token,
                 schemas=None):

        super().__init__(api_url, access_token, schemas)

        self.stocks = stocks.StockManager(
                self,
                schema=self.retrieve_schema(
                    stocks.StockManager))
        self.items = items.ItemManager(
                self,
                schema=self.retrieve_schema(
                    items.ItemManager))
