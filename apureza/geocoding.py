# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
from gistools.geocoding import DictionaryConverter, AddressBuilder

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'


class SinanConverter(DictionaryConverter):
    """ Class for converting addresses from SINAN database

    """

    def __init__(self, dictionary_file):
        super().__init__(dictionary_file)


class SinanBuilder(AddressBuilder):
    """ Class for building addresses from SINAN database

    """

    def __init__(self):
        super().__init__()

    def build(self, *args, **kwargs):
        pass
