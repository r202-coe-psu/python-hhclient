from hhclient.common import client

from . import stocks
from . import items
from . import inventories
from . import consumptions

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
        self.inventories = inventories.InventoryManager(
                self,
                schema=self.retrieve_schema(
                    inventories.InventoryManager))
        self.consumptions = consumptions.ConsumptionManager(
                self,
                schema=self.retrieve_schema(
                    consumptions.ConsumptionManager))
