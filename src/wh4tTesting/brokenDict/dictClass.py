#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

class dictClass(dict):
    
    var = ""
    # Static dictionary
    dictionaryStatic = {}
    
    def __init__(self,value):
        self.dictionaryDynamic = {}
        self.var = value
        self.dictionaryDynamic["var"] = value
        self.dictionaryStatic["var"] = value
        self["var"] = value
        
    def getVar(self): return self.var

    def getDynamicVarInDict(self): return self.dictionaryDynamic["var"]
    
    def getStaticVarInDict(self): return self.dictionaryStatic["var"]
    
    def getVarInClassDict(self): return self["var"]