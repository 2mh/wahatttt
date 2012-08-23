#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from codecs import open
from os.path import exists
from re import sub

from xml.etree import cElementTree as ET

from settings import getHashFile, getDefaultEncoding, get_de_en_bidix_file

class dict_from_file(dict):
    """
    This class represents a file as a dict, reading in all values pairwise,
    on each line.
    """
    def __init__(self, filename):
        dict.__init__(self)
        f = open(filename, "r", getDefaultEncoding())
        for line in f.readlines():
            pair = line.split()
            self[pair[0]] = float(pair[1])
        f.close()
        
class hashFile(file):
    """
    This class is a file class, specifically representing an hashsums file.
    It's used to encapsulate specifics about its name and existence.
    """
    def __init__(self, mode="r"):
        hashFile = getHashFile()
        
        if not exists(hashFile):
            print "Hash file doesn't exist."
            print "Create: " + hashFile
            try:
                open(hashFile, "w", getDefaultEncoding()).close()
            except Exception, e:
                print str(e)
        
        file.__init__(self, hashFile, mode)
   
class hashDict(dict):
    """
    This class is a dict class, used to handle the hash file above.
    Each entry in the hash file can be accessed through an object of
    this type.
    """
    def __init__(self):
        dict.__init__(self)
        f = hashFile()
        for line in f.readlines():
            pair = line.split()
            self[pair[0]] = pair[1]
        f.close()
    
    def save(self):
        """
        This method saves the contents of this class to disk.
        """
        f = hashFile(mode="w")
        for pair in self.items():
            f.write(' '.join(map(str, pair)) + '\n')
        f.close()
        
class en_to_de_dict(dict):
    """
    This dict provides a primitive dictionary from English to
    German words, w/o ambiguities (in turn w/o any special
    differentiation) used to increase semantic relatedness between
    the different documents we have.
    """
    def __init__(self):
        dict.__init__(self)
        de_en_bidix_file = get_de_en_bidix_file()
        xml_file_handler = ET.parse(de_en_bidix_file)
        p_elems = xml_file_handler.findall(".//p")
        # Only get (both-sided) single word 1:1 mappings
        p_elems_filtered = [p_elem for p_elem in p_elems
                            if len(p_elem.find("l").getchildren()) == 1
                            and len(p_elem.find("r").getchildren()) == 1]
        for p_elem in p_elems_filtered:
            # key: english word; val: german word
            self[p_elem.find("r").text] = p_elem.find("l").text
           
def normalize_word(word_to_normalize):
    """
    This function helps to normalize words in order to make
    them better comparable.
    @return: Normalized word as str type
    """
    
    # Transform umlauts to ASCII
    word = word_to_normalize.replace(u"Ä","Ae").replace(u"Ö","Oe"). \
        replace(u"Ü","Ue").replace(u"ä","ae").replace(u"ö","oe"). \
        replace(u"ü","ue").replace(u"ß","ss")
    # Remove stuff around words, like citation symbols, interpunctation
    # and return word
    return sub("\W+$", "", sub("^\W+", "", word))

def split_term(term):
    """
    This function splits a term into several words, e. g.
    "Diktatur-Kontrolle" will become ["Diktatur", "Kontrolle"]
    @param term:  A term to split being a string
    @return List with splitted words
    """
    return sub("[,-.&|]+", "#", term).split("#") # Split also "Dr.-Ing"
        
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

def clean_iterable(toClean):
    """
    @param toClean: An iterable whose elements should be freed from 
                    whitespaces.
    @return: Return iterable freed from whitespaces.
    """
    return map(lambda s : s.strip(), toClean)