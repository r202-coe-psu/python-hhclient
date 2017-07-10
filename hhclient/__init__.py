__version__ = '0.0.1'

from . import hhservices
from . import applications

def get_client(client_name):
    if client_name == 'hhservice':
        from .hhservices.client import Client
        return Client
    elif client_name == 'inventory':
        from .applications.inventories.client import Clinet
        return Client
    elif client_name == 'nutrition':
        from .applications.nutrition.client import Clinet
        return Client
