# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open

from settings import get_nouns_file, get_def_enc
from library import normalize_word

class Nouns(list):
    """
    This class holds a list of nouns for the German language, freely
    available from the Apertium RBMT project.
    """

    def __init__(self):
        """
        Reads in the nouns file and stores it.
        """
        list.__init__(self)
        
        f = open(get_nouns_file(), "r" ,get_def_enc())
        for noun in f.readlines():
            self.append(normalize_word(noun.strip()))
            
        f.close()
    
    def get_nouns(self):
        """
        @return: Returns all nouns stored.
        """
        return self