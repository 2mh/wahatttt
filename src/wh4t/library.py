#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from codecs import open
from os.path import exists

from settings import getHashFile
from settings import getDefaultEncoding

class hashFile(file):

    def __init__(self, mode="r"):
        hashFile = getHashFile()
        file.__init__(self, hashFile, mode)
        
        if not exists(hashFile):
            print "Hash file doesn't exist."
            print "Create: " + hashFile
            self = open(hashFile, "w", getDefaultEncoding())
            self.close()
   
class hashDict(dict):
    
    def __init__(self):
        f = hashFile()
        for line in f.readlines():
            pair = line.split()
            self[pair[0]] = pair[1]
        f.close()
    
    def save(self):
        f = hashFile(mode="w")
        for pair in self.items():
            f.write(' '.join(map(str, pair)) + '\n')
        f.close()    
            
def normalize_word(word_to_normalize):
    """
    This function helps to normalize words in order to make
    them better comparable.
    @return: Normalized word as str type
    """
    
    # Transform Umlauts
    return word_to_normalize.replace(u"Ä","Ae").replace(u"Ö","Oe"). \
        replace(u"Ü","Ue").replace(u"ä","ae").replace(u"ö","oe"). \
        replace(u"ü","ue").replace(u"ß","ss")
        
def rreplace(s, old, new, occurrence):
    """
    From public domain source by "mg.", 2010: 
    * http://stackoverflow.com/questions/2556108/
      rreplace-how-to-replace-the-last-occurence-of-an-expression-in-a-string
    
    Replaces a string from right to left (reverse) by allowing for
    specification of how many occurrences should be replaced.
    @param s: String to be altered.
    @param old: Substring to replace.
    @param new: New substring to put in place.
    @param occurrence: Number of substitutions (from right to left) to
                       carry out.
    @return: New string, after desired substitutions.
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)