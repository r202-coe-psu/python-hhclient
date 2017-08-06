from hhclient.common import base


class Consumption(base.Resource):
    __resource_name__ = 'consumptions'


class ConsumptionManager(base.Manager):
    __resource_class__ = Consumption
    __resource_url__ = '/stocks/{stock_id}/consumptions'

    def list(self, stock):
        url = self.__resource_url__.format(stock_id=stock.id)

        return self._list(url=url)
