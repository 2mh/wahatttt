#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

class dictClass(dict):
    
    var = ""
    dictionary = {}
    
    def __init__(self,value):
        self.var = value
        self.dictionary["var"] = value
        self["var"] = value
        
    def getVar(self): return self.var

    def getVarInDict(self): return self.dictionary["var"]
    
    def getVarInClassDict(self): return self["var"]