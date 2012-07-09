# -*- coding: utf-8 -*-

"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open
from settings import getMailBodySymbolsFile
from symbol import symbol
from settings import getDefaultEncoding
from settings import getMailBodyRawFile

class symbols:
    
    symbolSet = set()
    
    def __init__(self):
        pass
    
    def addSymbol(self,sym):
        self.symbolSet.append(sym)

    def createSymbolSet(self):
        
        # Only create if necessary
        if len(self.symbolSet) == 0: 
            
            f = open(getMailBodyRawFile(),"r",encoding=getDefaultEncoding())
        
            for sym in f.read(): 
                symObj = symbol(sym) 
                self.symbolSet.add(symObj)
        
            f.close()

        
    def writeSymbolsFile(self):
    
        self.createSymbolSet()
    
        f = open(getMailBodySymbolsFile(),"w",encoding=getDefaultEncoding())
             
        for char in sorted(self.symbolSet,reverse=True):
            f.write(char)
        f.close()
        
            
    def getNumberOfSymbols(self): return len(self.symbolSet)
