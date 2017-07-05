from . import base


class Building(base.Resource):
    __resource_name__ = 'buildings'


class BuildingManager(base.Manager):
    __resource_class__ = Building
    __resource_url__ = '/buildings'
