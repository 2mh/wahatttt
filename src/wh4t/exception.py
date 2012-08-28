# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

class VoidStructureError(Exception):
    """
    
    VoidStructureError exception is raised when some argument
    is received somewhere, which leads to problems (e. g.
    ZeroDivisionError or similar), because it's not
    designed to handle e. g. empty lists.
    
    """
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)