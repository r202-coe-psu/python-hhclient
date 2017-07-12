from hhclient.common import base
# from . import roles


class Inventory(base.Resource):
    __resource_name__ = 'inventories'


class InventoryManager(base.Manager):
    __resource_class__ = Inventory
    __resource_url__ = '/inventories'
