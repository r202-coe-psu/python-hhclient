'''
Created on Feb 26, 2013

@author: boatkrap
'''

import urllib

from . import schemas


class Error:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Resource:
    def __init__(self, **kwargs):
        self.errors = []
        self.response = kwargs.pop('response', {})

        if 'error' in kwargs:
            kws = kwargs.pop('error')
            self.update_error(**kws)

        if 'errors' in kwargs:
            kws = kwargs.pop('errors')
            self.update_errors(kws)

        self.data = {k.replace('_','-'): v for k, v in kwargs.items()}

        if 'id' not in self.data:
            self.data['id'] = None

    @property
    def is_error(self):
        if len(self.errors):
            return True

        return False

    def update_error(self, **kwargs):
        self.errors.append(Error(**kwargs))

    def update_errors(self, errors):
        for kwe in errors:
            self.update_error(**kwe)

    def __setattr__(self, name, value):
        if name in ['data', 'errors', 'response']:
            self.__dict__[name] = value
        else:
            if '_' in name:
                name = name.replace('_', '-')
            self.data[name] = value

    def __getattr__(self, name):
        nname = name.replace('_', '-')

        if nname in self.data:
            return self.data[nname]

        if name in self.__dict__:
            return self.__dict__[name]

        raise AttributeError(name)

    def get(self):
        # set_loaded() first ... so if we have to bail, we know we tried.
        self.set_loaded(True)
        if not hasattr(self.manager, 'get'):
            return

        new = self.manager.get(self.id)
        if new:
            # print("new._info:", new._info)
            self._add_details(new._info)
            for (k, v) in new._info.items():
                self._info[k] = v

    def is_loaded(self):
        return self._loaded

    def set_loaded(self, val):
        self._loaded = val


class BaseManager:

    __resource_class__ = None
    __resource_url__ = None

    def __init__(self, api, schema):
        self.api = api
        self.schema_data = schema
        self.schema = schemas.ResourceSchemaFactory.create_schema(
                self.__resource_class__.__resource_name__,
                schema)

    def get_resource_class(self):
        return self.__resource_class__

    def get_data(self, resource):
        return resource

    def _list(self, url=None, params={}):
        url = self.resource_url(url, params=params)
        response, status_code = self.api.http_client.get(url)
        resource_dict = self.schema.load(response, many=True)
    
        errors = []

        if 'errors' in response:
            errors = response['errors']

        # print('rd', resource_dict)

        response_list = [self.__resource_class__(errors=errors,
                                                 response=data,
                                                 **data)\
                            for data in resource_dict.data]
        return response_list

    def _get(self, resource_id, url=None, params={}):
        url = self.resource_url(url, resource_id=resource_id, params=params)
        response, status_code = self.api.http_client.get(url)
        # print('response', response)
        resource_dict = self.schema.load(response)
    
        errors = []

        if 'errors' in response:
            errors = response['errors']
        # print('rd:', resource_dict)
        return self.__resource_class__(errors=errors,
                                       response=response,
                                       **resource_dict.data)



    def _delete(self, url=None, params={}):
        response = self.api.http_client.delete(url)

    def _create(self, resource, url=None, params={}):
        url = self.resource_url(url, params=params)
        data = self.schema.dump(resource).data
        response, status_code = self.api.http_client.post(url, data=data)
        resource_dict = self.schema.load(response)
    
        errors = []

        if 'errors' in response:
            errors = response['errors']

        return self.__resource_class__(errors=errors, **resource_dict.data)

    def _update(self, resource, url=None, params={}):
        url = self.resource_url(url, params=params)
        data = self.schema.dump(resource).data
        response, status_code = self.api.http_client.put(url, data=data)
        resource_dict = self.schema.load(response)
    
        errors = []

        if 'errors' in response:
            errors = response['errors']

        return self.__resource_class__(errors=errors, **resource_dict.data)

    def resource_url(self, url, resource_id=None, params={}):
        url = url if url else self.__resource_url__
        if resource_id:
            url = url + '/' + str(resource_id)
        if len(params) > 0:
            url = url + '?' + urllib.urlencode(params)

        # if url[-1] != '/':
        #     url = url + '/'

        return url


class Manager(BaseManager):
    
    def list(self):
        return self._list()

    def create(self, **kwargs):
        resource = self.__resource_class__(**kwargs)
        return super()._create(resource)

    def get(self, resource_id):
        return super()._get(resource_id)

    def update(self, resource):
        return super()._update(resource)

    def delete(self, resource):
        return super()._delete(resource)
