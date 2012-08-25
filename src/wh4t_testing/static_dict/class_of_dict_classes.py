# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open
from dict_class import DictClass

from src.wh4t.settings import  get_def_enc

class ClassOfDictClasses:
    
    dict_classes = []
    
    def __init__(self):
        f = open("in_file","r", get_def_enc())
        for line in f.readlines():
            dc = DictClass(line)
            self.dict_classes.append(dc)
        f.close()
            
    def write_out_var_file(self):
        f = open("out_var_file","w", get_def_enc())
        for dc in self.dict_classes:
            f.write(dc.getVar())
        f.close()
        
    def write_out_static_var_in_dict_file(self):
        f = open("out_static_var_in_dict_file","w", get_def_enc())
        for dc in self.dict_classes:
            f.write(dc.getStaticVarInDict())
        f.close()
            
    def write_out_dynamic_var_in_dict_file(self):
        f = open("out_dynamic_var_in_dict_file","w", get_def_enc())
        for dc in self.dict_classes:
            f.write(dc.getDynamicVarInDict())
        f.close()
            
    def write_out_var_in_class_dict_file(self):
        f = open("out_var_in_class_dict_file","w", get_def_enc())
        for dc in self.dict_classes:
            f.write(dc.getVarInClassDict())
        f.close()