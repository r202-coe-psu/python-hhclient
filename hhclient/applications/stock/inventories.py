from hhclient.common import base
from hhclient.common import schemas


class InventoryConsumingItem(base.Resource):
    __resource_name__ = 'inventory-consuming-items'


class Inventory(base.Resource):
    __resource_name__ = 'inventories'


class InventoryManager(base.Manager):
    __resource_class__ = Inventory
    __resource_url__ = '/stocks/{stock_id}/inventories'

    def __init__(self, api, schema):
        super().__init__(api, schema)
        self.inventoy_consuming_item_schema = \
            schemas.ResourceSchemaFactory.create_schema(
                InventoryConsumingItem,
                self.api.retrieve_schema(
                    resource_type=InventoryConsumingItem.__resource_name__))

    def create(self, stock, **kwargs):
        url = self.__resource_url__.format(stock_id=stock.id)

        inventory = Inventory(**kwargs)
        return self._create(inventory, url=url)

    def list(self, stock):
        url = self.__resource_url__.format(stock_id=stock.id)

        return self._list(url=url)

    def list_items(self, stock):
        url = '{}/list-items'.format(
                self.__resource_url__.format(
                    stock_id=stock.id))

        return self.api.items._list(url=url)

    def consume(self, stock, item, consuming_size, consuming_unit=None):
        url = '{}/consume'.format(
                self.__resource_url__.format(
                    stock_id=stock.id))

        data = dict(item=item,
                    consuming_size=consuming_size,
                    consuming_unit=consuming_unit)

        consuming_data = self.inventory_consuming_item_schema.dump(data).data
        response, status_code = self.api.http_client.post(url, data=data)
        resource_dict = self.inventory_consuming_item_schema.load(response)

        errors = []

        if 'errors' in response:
            errors = response['errors']

        return self.__resource_class__(errors=errors, **resource_dict.data)

