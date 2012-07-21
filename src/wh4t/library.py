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
    return word_to_normalize.replace("Ä","Ae").replace("Ö","Oe"). \
        replace("Ü","Ue").replace("ä","ae").replace("ö","oe"). \
        replace("ü","ue").replace("ß","ss")