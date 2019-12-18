# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
from gistools.geocoding import DictionaryConverter

__author__ = 'Benjamin Pillot'
__copyright__ = 'Copyright 2019, Benjamin Pillot'
__email__ = 'benjaminpillot@riseup.net'


class SinanConverter(DictionaryConverter):
    """ Class for converting addresses from SINAN database

    """

    _converter = dict(L12={'quadra': r"(\bQ(?:C(?![UADR])|N(?![UADR]))?U?A?D?R?A?\.*\s*)(\d+)"},
                      L13={'conjunto': r"(\bCO?N?J?U?N?T?O?\.*\s*)(\w+)"},
                      L14={'rua': r"(\bRU?A?\.*\s*)(\w+)",
                           'avenida': r"(\bAVE?N?I?D?A?\.*\s*)(\w+)"})

    def __init__(self, dictionary_file):
        super().__init__(dictionary_file)


