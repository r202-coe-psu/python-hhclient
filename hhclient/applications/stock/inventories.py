from hhclient.common import base


class Inventory(base.Resource):
    __resource_name__ = 'inventories'


class InventoryManager(base.Manager):
    __resource_class__ = Inventory
    __resource_url__ = '/stocks/{stock_id}/inventories'

    def create(self, stock, **kwargs):
        url = self.__resource_url__.format(stock_id=stock.id)

        inventory = Inventory(**kwargs)
        return self._create(inventory, url=url)

    def list(self, stock):
        url = self.__resource_url__.format(stock_id=stock.id)

        return self._list(url=url)
