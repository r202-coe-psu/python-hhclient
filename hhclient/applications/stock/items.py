from hhclient.common import base


class Item(base.Resource):
    __resource_name__ = 'items'


class ItemManager(base.Manager):
    __resource_class__ = Item
    __resource_url__ = '/items'
