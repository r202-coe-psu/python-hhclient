from . import base


class Building(base.Resource):
    __resource_name__ = 'buildings'


class BuildingManager(base.Manager):
    __resource_class__ = Building
    __resource_url__ = '/buildings'

    def active_application(self, building_id, application_id):
        url = '{}/{}/applications'.format(self.__resource_url__,
                                       building_id)

        data = dict(id=application_id)
        app_data = self.api.applications.schema.dump(data).data

        response, status_code = self.api.http_client.put(url,
            data=app_data)

