#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open
from dictClass import dictClass

class classOfDictClasses:
    
    dictClasses = []
    
    def __init__(self):
        f = open("inFile.txt","r","utf-8")
        for line in f.readlines():
            dc = dictClass(line)
            self.dictClasses.append(dc)
        f.close()
            
    def writeOutVarFile(self):
        f = open("outVarFile.txt","w","utf-8")
        for dc in self.dictClasses:
            f.write(dc.getVar())
        f.close()
        
    def writeOutVarInDictFile(self):
        f = open("outVarInDictFile.txt","w","utf-8")
        for dc in self.dictClasses:
            f.write(dc.getVarInDict())
            
    def writeOutVarInClassDictFile(self):
        f = open("outVarInClassDictFile.txt","w","utf-8")
        for dc in self.dictClasses:
            f.write(dc.getVarInClassDict())