from hhclient.common import base


class Item(base.Resource):
    __resource_name__ = 'items'


class ItemManager(base.Manager):
    __resource_class__ = Item
    __resource_url__ = '/items'

    def get_upc(self, upc):
        url = '{}/upc/{}'.format(self.__resource_url__,
                                 upc)

        item = super()._get(resource_id=None, url=url)
        return item
