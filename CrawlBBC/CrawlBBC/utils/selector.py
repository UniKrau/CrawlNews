#!/usr/bin/python
# -*- coding: utf-8 -*-

# __author__ 'Hao LI'

import types

from w3lib.html import replace_entities
from urlparse import urlparse, urljoin

NULL = [None, 'null']

prefix = "www.bbc"

new_prefix = "http://www.bbc.com"

def clean_link(link_text):
    """
        Remove leading and trailing whitespace and punctuation
    """

    return link_text.strip("\t\r\n '\"")

clean_url = lambda base_url,u,response_encoding: urljoin(base_url,
                                                         replace_entities(clean_link(u.decode(response_encoding))))
"""
    remove leading and trailing whitespace and punctuation and entities from the given text.
    then join the base_url and the link that extract
"""
