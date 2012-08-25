# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

class DictClass(dict):
    
    var = ""
    # Static dictionary
    dict_static = {}
    
    def __init__(self,value):
        self.dict_dynamic = {}
        ### Uncommenting the following, self.dict_static turns dynamic
        #self.dict_static = {}
        self.var = value
        self.dict_dynamic["var"] = value
        self.dict_static["var"] = value
        self["var"] = value
        
    def getVar(self): return self.var

    def getDynamicVarInDict(self): return self.dict_dynamic["var"]
    
    def getStaticVarInDict(self): return self.dict_static["var"]
    
    def getVarInClassDict(self): return self["var"]