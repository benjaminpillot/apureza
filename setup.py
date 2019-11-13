# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

import apureza

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'


with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(name='gis_tools',
      version=apureza.__version__,
      description='Apureza project API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/benjaminpillot/apureza',
      author='Benjamin Pillot',
      author_email='benjaminpillot@riseup.net',
      install_requires=parse_requirements("requirements.txt", session='hack'),
      python_requires='>=3',
      license='GNU GPL v3.0',
      packages=find_packages(),
      zip_safe=False)

