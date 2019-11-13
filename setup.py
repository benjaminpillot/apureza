# -*- coding: utf-8 -*-

""" Module summary description.

Setup installation for apureza package.

N.B.:
We may use "parse_requirements" function (from pip._internal.req)
to build the "install_requires" key of setup dict from the file
"requirements.txt" but I'm not sure it's a good practice.
"""
from setuptools import setup, find_packages

import apureza

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'


with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(name='apureza',
      version=apureza.__version__,
      description='Apureza project API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/benjaminpillot/apureza',
      author='Benjamin Pillot',
      author_email='benjaminpillot@riseup.net',
      install_requires=['numpy>=1.17.2',
                        'Keras>=2.3.1',
                        'scipy>=1.1.0',
                        'matplotlib>=3.0.3',
                        'scikit_learn>=0.21.3'],
      python_requires='>=3',
      license='GNU GPL v3.0',
      packages=find_packages(),
      zip_safe=False)

