# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from codecs import open
from os.path import exists
from re import sub, match
from sys import stdout

from nltk.text import TextCollection
from progressbar import ProgressBar
from xml.etree import cElementTree as ET

from settings import get_hash_file, get_def_enc, get_stems_file, \
                     get_de_en_bidix_file, get_synsets_file, \
                     get_tfidf_matrix_file

class DictFromFile(dict):
    """
    This class represents a file as a dict, reading in all values 
    pairwise, on each line.
    """
    def __init__(self, filename):
        dict.__init__(self)
        f = open(filename, "r", get_def_enc())
        for line in f.readlines():
            pair = line.split()
            self[pair[0]] = float(pair[1])
        f.close()
        
class HashFile(file):
    """
    This class is a file class, specifically representing an 
    hashsums file.
    It's used to encapsulate specifics about its name and existence.
    """
    def __init__(self, mode="r"):
        hash_file = get_hash_file()
        
        if not exists(hash_file):
            print "Hash file doesn't exist."
            print "Create: " + hash_file
            try:
                open(hash_file, "w", get_def_enc()).close()
            except Exception, e:
                print str(e)
        
        file.__init__(self, hash_file, mode)
   
class HashDict(dict):
    """
    This class is a dict class, used to handle the hash file above.
    Each entry in the hash file can be accessed through an object of
    this type.
    """
    def __init__(self):
        dict.__init__(self)
        f = HashFile()
        for line in f.readlines():
            pair = line.split()
            self[pair[0]] = pair[1]
        f.close()
    
    def save(self):
        """
        This method saves the contents of this class to disk.
        """
        f = HashFile(mode="w")
        for pair in self.items():
            f.write(' '.join(map(str, pair)) + '\n')
        f.close()
        
class EnToDeDict(dict):
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
            # in lower-case & normalized writing
            self[p_elem.find("r").text.lower()] = \
                normalize_word(p_elem.find("l").text.lower())
                
class Synsets(list):
    """
    This list holds synsets, i. e. words semantically grouped with
    each other.
    """
    def __init__(self):
        list.__init__(self)
        synsets_file = get_synsets_file()
        f = open(synsets_file, "r", get_def_enc())
        lines = f.readlines()
        f.close()
        
        for line in lines:
            if line[0] == "#":
                continue
            synset = self._clean_synset(line.split(";"))
            if len(synset) >= 2:
                self.append(synset)
            
    def _clean_synset(self, synset):
        """
        Internal method which removes certain expressions from
        a synset.
        @param: Synset (as list)
        @return: A clean synset (as list)
        """
        clean_synset = list()
        lang_levels = ["umgangssprachlich", "derb", "vulgär", 
                       "fachsprachlich", "gehoben"]
        for word in synset:
            for lang_level in lang_levels:
                word = sub(" \("+lang_level+"\)", "", word)
            if match(".*[ \(\)].*", word) == None:
                clean_synset.append(normalize_word(word.lower()))
                
        return clean_synset
           
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
      rreplace-how-to-replace-the-last-occurence-of-an
      -expression-in-a-string
    
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

def clean_iterable(iter_to_clean):
    """
    @param iter_to_clean: An iterable whose elements should be freed from 
                    whitespaces.
    @return: Return iterable freed from whitespaces.
    """
    return map(lambda s : s.strip(), iter_to_clean)

def get_nltk_text_collection(xmlcollection):
    """
    @param xmlcollection: A collection of all (as of now) XML documents,
                          of type collection.
    @return: Retrieves an NLTK TextCollection with all stems from our 
             document collection.
    """
    nltk_textcollectionList = list()
    
    print "Creating NLTK text collection ... "
    xmlcollection_list = xmlcollection.get_docs()
    
    pb = ProgressBar(maxval=len(xmlcollection_list)).start()
    cnt = 0
    for doc in xmlcollection_list:
        cnt += 1
        pb.update(cnt)
        nltk_textcollectionList.append(list(doc.get_stems()))
        
    return TextCollection(nltk_textcollectionList)

def get_classification_stems(stems, idf_dict):
    """
    This function removes most frequent and all very rare stems (single
    occurrence), to improve classification results.
    @param stems: List of stems to be filtered
    @param idf_dict: Dictionary containing the idf values to filter
                     after
    @return: List with out-filtered stems
    """ 
    max_val = max(idf_dict.itervalues()).as_integer_ratio()
    return [stem for stem in stems
            if idf_dict[stem] > 2.0
            and not idf_dict[stem].as_integer_ratio() == max_val]

def write_tfidf_file(xmlcollection, nltk_textcollection):
    """
    Writes a tf*idf matrix file with all tf*idf values for each 
    document, row by row. The columns represent the (alphabetically
    ordered) stems available in the whole collection.
    @param xmlcollection: Collection of XML documents, type collection
    @param nltk_textcollection: NLTK TextCollection of all the stems
    """
    idf_file = get_stems_file(measure="_idf")
    avg_words_per_doc = len(xmlcollection.get_words()) / \
                        len(xmlcollection.get_docs())

    if not exists(idf_file):
        write_idf_file(xmlcollection, nltk_textcollection)

    idf_dict = DictFromFile(idf_file)
    high_tfidf_stems = set()
    
    collection_stems = list(xmlcollection.get_stems(uniq=True))
    print "Length of collection, all stems:", len(collection_stems)
    
    # Remove most frequent (idf<2) / stop stems (or qualifying 
    # as such), and most rare stems (max(idf)), as they are of no 
    # help to separate / make up clusters
    collection_stems = get_classification_stems(collection_stems, idf_dict)
    print "Length of collection, cluster stems:", len(collection_stems)
    
    f = open(get_tfidf_matrix_file(), "w", get_def_enc())
    for doc in xmlcollection.get_docs():
        doc_stems = doc.get_stems()
        col = TextCollection("")
        
        stdout.write(doc.get_id())
        idf_row = ""
        stdout.write(" (")
        for stem in sorted(collection_stems):
            tf = col.tf(stem, doc_stems)
    
            # Reweight tf values, to get more classifcation words
            # and compensate for the very different document sizes 
            # available
            # Idea: Accounts for average document length, but also for
            # the number of times a word effictively occurs in a 
            # specific document; other variations can be thought of 
            # (using log) or maximal tf values
            # Note: The clustering works better with (in general)
            # smaller values
            if tf > 0.0:
                tf = 1.0 / avg_words_per_doc * tf
            # If nothing applies: tf is 0.0
                
            tfidf = tf*float(idf_dict[stem])
            if (tfidf > 0.0):
                stdout.write(stem + ", ")
                high_tfidf_stems.add(stem)
            idf_row += str(tfidf) + " "
        f.write(idf_row + "\n")
        stdout.write(")\n")
    f.close()
    print "List length of high value tf*idf terms:", len(high_tfidf_stems)
  
def write_idf_file(xmlcollection, nltk_textcollection):
    """
    Writes a (collection-wide) file with idf valus for each stem.
    @param xmlcollection: Collection of XML documents, type collection
    @param nltk_textcollection: NLTK TextCollection of all the stems
    """
    print "Calculating idf values for all stems ..."
    all_stems = xmlcollection.get_stems(uniq=True)
    idfset = set()
    pb = ProgressBar(maxval=len(all_stems)).start()
    cnt = 0
    for word in all_stems:
        cnt += 1
        pb.update(cnt)
        idf = nltk_textcollection.idf(word)
        if idf > 0.0: 
            idfset.add((idf, word))
    
    f = open(get_stems_file(measure="_idf"), "w", get_def_enc())
    for pair in sorted(idfset, reverse=True): 
        f.write(pair[1] + " " + str(pair[0]) + "\n")
    f.close()