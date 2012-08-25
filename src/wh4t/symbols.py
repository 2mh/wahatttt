# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open

from settings import get_symbols_file, get_def_enc, get_raw_file

class Symbols(dict):
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
        dict.__init__(self)
        self._create_symbols_dict()

    def _create_symbols_dict(self):
        """
        Opens a file (for now) with all text available and stores its
        symbols as keys (for each of whom a determined attribute is stored
        as value). Meant as internal method.
        """     
        f = open(get_raw_file(), "r", encoding=get_def_enc())
        
        # Get unique symbols first
        symset = set()
        for sym in f.read():
            symset.add(sym)
            
        # For each symbol (key) determine an attribute to store in this
        # instance
        for sym in symset:
            symobj = self._classify_symbol(sym) 
            self.__setitem__(sym, symobj.get(sym))
    
        f.close()
     
    def write_symbols(self):
        """ 
        Writes a file with all the symbols (i. e. this class's keys)
        in order.
        """
        f = open(get_symbols_file(), "w", encoding=get_def_enc())
             
        for symbol in sorted(self.keys(), reverse=True):
            f.write(symbol)
            
        f.close()
             
    def get_no_of_symbols(self): 
        """
        @return: The number of unique symbols (stored in this class)
                 available.
        """
        return len(self)
    
    def _classify_symbol(self, symbol):
        """
        @return: For each symbol this (internal) method returns this
                 symbol as key together with its attribute (set) as
                 value.
        """
    
        # Categories where symbols (most specifically) may belong to
        ALPHA = "alpha" # E. g. "a", "B", but also "ä" or "Ö"
        DIGIT = "digit" # 0-9
        PUNCT = "interpunctuation" # E. g. ",", "'" or "("
        WHITE = "whitespace" # E. g. " ", \t or \n
        MATH = "mathematics" # E. g. "-", "+" or "^"
        COMP = "computer" # E. g. things like "/", "\", or "#"
        LAW = "law" # E. g. "§" or "©"
        MONEY = "money" # E. g. "$" or "£"
        UNDEF = "undefined" # For everything lasting
        
        symbol_class = set()
        
        # Assign a symbol its symbolic class(es)
        if symbol.isalpha():
            symbol_class.add(ALPHA)
        if symbol.isdigit():
            symbol_class.add(DIGIT)
        if symbol in u"'\"`,.:»«-´;?![]()":
            symbol_class.add(PUNCT)
        if symbol in u"+-*/=:^{}[]()!><|·%":
            symbol_class.add(MATH)
        if symbol in u"#+-*=_/\\^[](){}:$!~><|@&%":
            symbol_class.add(COMP)    
        if symbol in u" \t\n":
            symbol_class.add(WHITE)
        if symbol in u"£$":
            symbol_class.add(MONEY)
        if symbol in u"§©":
            symbol_class.add(LAW)
        if len(symbol_class) == 0:
            symbol_class.add(UNDEF)
        
        return {symbol:symbol_class}