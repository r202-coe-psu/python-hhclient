'''
HH-service
----------

A service core for HomeHero
'''

import re
import ast
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('hhclient/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))
setup(
    name='hhclient',
    version=version,
    url='',
    license='',
    author='',
    author_email='',
    description='A Home Hero service client',
    long_description=__doc__,
    packages=['hhclient'],
    include_package_data=True,
    install_requires=[
        'requests',
        'marshmallow-jsonapi'
    ],
    classifiers=[
    ],
)

