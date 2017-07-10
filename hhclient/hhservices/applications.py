from ..common import base
# from . import roles


class Application(base.Resource):
    __resource_name__ = 'applications'


class ApplicationManager(base.Manager):
    __resource_class__ = Application
    __resource_url__ = '/applications'

    def list(self):
        return self._list()

    def get(self, app_id):
        return self._get(app_id)
