import requests
import json
import logging

logger = logging.getLogger(__name__)

from . import users

class HTTPClient:
    def __init__(self, username=None, password=None,
                 host='127.0.0.1', port=8080,
                 secure_connection=False,
                 token=None):

        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.secure_connection = secure_connection
        self.auth_token = token
        self.user_id = None

        self.scheme = 'http'
        if self.secure_connection:
            self.scheme = 'https'

        self.session = requests.session()

        self.api_url = '%s://%s:%d' % (self.scheme, self.host, self.port)

    def authenticate(self):
        body = {'password_credentials': {'password': self.password,
                                         'username': self.username}}

        response = self.post('/authentication/tokens',
                                'POST',
                                body=body,
                                headers={})
        if response:
            self.auth_token = response['access']['token']['id']
            self.user_id = response['access']['user']['id']
            return response
        return None

    def request(self, url, method, **kwargs):
        kwargs['headers']['Content-Type'] = 'application/vnd.api+json'

        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])

        logger.debug(method + url + '\nargs:' + str(kwargs))
        response = self.session.request(method, 
                                    url,
                                    **kwargs)


        logger.debug('response => code: {} data: {}'\
                .format(response.status_code, response.json()))

        return response.json(), response.status_code


    def _cs_request(self, url, method, **kwargs):
        # if self.auth_token is None:
        #     self.authenticate()

        kwargs.setdefault('headers', {})['X-Auth-Token'] = self.auth_token

        return self.request(self.api_url + url, 
                            method,
                            **kwargs)

    def get(self, url, **kwargs):
        return self._cs_request(url, 'GET', **kwargs)

    def post(self, url, **kwargs):
        return self._cs_request(url, 'POST', **kwargs)

    def put(self, url, **kwargs):
        return self._cs_request(url, 'PUT', **kwargs)

    def delete(self, url, **kwargs):
        return self._cs_request(url, 'DELETE', **kwargs)


class Client:
    def __init__(self, username=None, password=None,
                 host='127.0.0.1', port=80,
                 secure_connection=False,
                 token=None):

        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.secure_connection = secure_connection

        self.http_client = HTTPClient(username,
                                      password,
                                      host,
                                      port,
                                      secure_connection,
                                      token
                                      )

        schemas = self.get_schemas()

        self.users = users.UserManager(self,
                schema=schemas.get(users.UserManager.__resource_class__.__resource_name__, None))
    
    def authenticate(self):
        return self.http_client.authenticate()

    def get_schemas(self):
        response, status_code = self.http_client.get('/schemas')
        return response
