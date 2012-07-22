#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

def normalize_word(word_to_normalize):
    """
    This function helps to normalize words in order to make
    them better comparable.
    @return: Normalized word as str type
    """
    
    # Transform Umlauts
    return word_to_normalize.replace(u"Ä","Ae").replace(u"Ö","Oe"). \
        replace(u"Ü","Ue").replace(u"ä","ae").replace(u"ö","oe"). \
        replace(u"ü","ue").replace(u"ß","ss")