#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open

from settings import getNounsFile
from settings import getDefaultEncoding
from library import normalize_word

class nouns(list):
    """
    This class holds a list of nouns for the German language, freely
    available from the Apertium RBMT project.
    """

    def __init__(self):
        """
        Reads in the nouns file and stores it.
        """
        f = open(getNounsFile(),"r",getDefaultEncoding())
        for noun in f.readlines():
            self.append(normalize_word(noun.strip()))
    
    def getNouns(self):
        """
        @return: Returns all nouns stored.
        """
        return self