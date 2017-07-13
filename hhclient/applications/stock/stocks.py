from hhclient.common import base
# from . import roles


class Stock(base.Resource):
    __resource_name__ = 'stocks'


class StockManager(base.Manager):
    __resource_class__ = Stock
    __resource_url__ = '/stocks'
