#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open

from settings import getMailBodySymbolsFile
from settings import getDefaultEncoding
from settings import getMailBodyRawFile

class symbols(dict):
    """
    This class stores all symbols available in the document collection,
    as keys. The corresponding values represent attributes, which these
    symbols have. For instance, the symbol "a" is an "alpha" symbol.
    
    It's assumed that this information might be useful to determine of
    which type a document is. E. g. if it is made up mainly of
    non-ASCII symbols it's either written in a language with lots of
    other symbols, or: probably the document is full of "garbage", thus
    from a linguistic POV not interesting and worth classifying.
    """
    
    def __init__(self):
        """
        At instantiation all available symbols get created.
        """
        self._createSymbolsDict()

    def _createSymbolsDict(self):
        """
        Opens a file (for now) with all text available and stores its symbols
        as keys (for each of whom a determined attribute is stored as value).
        Meant as internal method.
        """     
        f = open(getMailBodyRawFile(), "r", encoding=getDefaultEncoding())
        
        # Get unique symbols first
        symSet = set()
        for sym in f.read():
            symSet.add(sym)
            
        # For each symbol (key) determine an attribute to store in this 
        # instance
        for sym in symSet:
            symObj = self._classifySymbol(sym) 
            self.__setitem__(sym, symObj.get(sym))
    
        f.close()
     
    def writeSymbolsFile(self):
        """ 
        Writes a file with all the symbols (i. e. this class's keys)
        in order.
        """
        f = open(getMailBodySymbolsFile(), "w", encoding=getDefaultEncoding())
             
        for symbol in sorted(self.keys(), reverse=True):
            f.write(symbol)
        f.close()
             
    def getNumberOfSymbols(self): 
        """
        @return: The number of unique symbols (stored in this class)
                 available.
        """
        return len(self)
    
    def _classifySymbol(self, symbol):
        """
        XXX: To be implemented.
        @return: For each symbol this class return this symbol
                 as key together with its attribute as value.
        Meant as class internal method.    
        """
        
        """
        XXX: Under development ...
        # Categories
        ALPHA = "alpha" # e. g. "a", "B", but also "ä" or "Ö"
        DIGIT = "digit" # 0-9
        UNDEF = "undefined"
        
        symbolClass = UNDEF
        
        # Check if it's an symbol considered ALPHA
        if symbol.isalpha() or symbol in "äöüÄÖÜ": 
            symbolClass = ALPHA
        
        return {symbol:symbolClass}
        """
        return {symbol:None}