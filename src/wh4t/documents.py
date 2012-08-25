#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open
from os import listdir
from collections import defaultdict

from nltk.probability import FreqDist
from nltk.metrics import edit_distance
from progressbar import ProgressBar

from document import document
from listByLen import ListByLen
from settings import get_mailfolder, get_tokens_file, get_def_enc, \
                     get_types_file, get_raw_file, get_words_file, \
                     get_stems_file, get_words_by_editdistance_file, \
                     get_topwords_file, get_def_no_of_topwords, \
                     get_def_len_for_editdistancing, \
                     get_def_editdistance_filename_suffix
from nouns import Nouns

class Collection(dict):
    """
    This class is to hold a collection of documents, which
    are of type document. This class is a dict in order to
    avoid having static variables. Thus different collections
    of documents can be created, e. g. a collection containing
    all documents available and another one only feat. documents
    of Wau or a real subset of them.
    """        
    
    ############################################################
    # Key names used to store values in an object of this class.
    # See __init__ method below for some more explanation.
    ############################################################
    
    DOC_LIST = "doc_list"
    TEXT = "text"
    TOKENS = "tokens"
    TYPES = "types"
    TYPES_LOWERED = "types_lowered"
    WORDS = "words"
    STEMS = "stems"
    STEMS_UNIQ = "stems_uniq"
    WORDS_BY_EDITDISTANCE = "words_by_edit_distance"
    TOPWORDS = "topwords"
    TEXT_FREQDIST = "text_freqdist"    
    NOUNS = "nouns"
    REF_NOUNS = "ref_nouns" 
    DOCS_COUNT = "docs_count"
        
    def __init__(self):
        """
        Initialization of key-value pairs to hold the collection
        of documents.
        """
        dict.__init__(self)
        
        # For holding a list of documents
        self.__setitem__(self.DOC_LIST, list())

        # For holding the collection's raw text
        self.__setitem__(self.TEXT, str())
        
        # For holding all of the text tokenized by NLTK
        self.__setitem__(self.TOKENS, list())
        
        # For holding the types of the collection
        self.__setitem__(self.TYPES, set())
        
        # For holding the lowered types of the collection
        self.__setitem__(self.TYPES_LOWERED, set())
        
        # For holding a list of all the words, i. e. the cleaned
        # tokens; the words are not necessarily unique 
        self.__setitem__(self.WORDS, list())
        
        # For holding a list of all the stems
        self.__setitem__(self.STEMS, list())
        
        # # For holding a set of all the stems; unique values
        self.__setitem__(self.STEMS_UNIQ, set())
        
        # For holding unique pairs of words being of some edit distance
        self.__setitem__(self.WORDS_BY_EDITDISTANCE, set())
        
        # For holding a specified amount of most frequent words, along
        # with each frequency as absolute number.
        self.__setitem__(self.TOPWORDS, defaultdict())
        
        # To hold an object with the frequencies of all words
        self.__setitem__(self.TEXT_FREQDIST, None)
        
        # To hold all nouns found, in a list (for frequency analysis)
        self.__setitem__(self.NOUNS, list())
        
        # Initializes a nouns object (is a list) of reference nouns 
        # we use to find nouns in the collection
        self.__setitem__(self.REF_NOUNS, Nouns())
        
        # Read in all documents
        # XXX: This part may change in its behaviour soon
        fileslist = listdir(get_mailfolder())
        for xml_filename in fileslist:
            xmldoc = document(get_mailfolder() + xml_filename)
            self[self.DOC_LIST].append(xmldoc)
            
        # Store number of files found
        self.__setitem__(self.DOCS_COUNT, len(fileslist))
        
    def get_doc(self, pos): 
        """
        @param pos: The position (int) of the document in the list.
        @return: A specific document (of type document)
        """
        return self[self.DOC_LIST][pos]
    
    def get_docs(self): 
        """
        @return: List of all documents in this collection, sorted by
                 name (ASCII encoding order)
        """
        return sorted(self[self.DOC_LIST], key=lambda doc: doc.get_id())
    
    def get_filesize(self):
        """
        @return: Size of all files (in bytes) of the collection, 
                 including all (meta) data
        """
        dir_totsize = 0
        for doc in self.get_docs():
            dir_totsize += doc.get_filesize()
        return dir_totsize
    
    def get_rawsize(self):
        """
        @return: Size of only the body content parts of the collection
        """
        dir_netsize = 0
        for doc in self.get_docs():
            dir_netsize += doc.get_rawlen()
        return dir_netsize
    
    def get_text(self):
        """
        @return: Return as a string all the documents' body content, in
                 the given raw form; do the retrieval only once
        """
        if len(self[self.TEXT]) == 0:
            for doc in self.get_docs():
                self[self.TEXT] += doc.get_rawcontent()      
        return self[self.TEXT]
    
    def get_tokens(self):
        """
        @return: A list of all tokens found in the collection and 
                 ordered as is. Ensure to get the tokens once only.
        """
        if len(self[self.TOKENS]) == 0:
            for doc in self.get_docs():
                for token in doc.get_tokens():
                    self[self.TOKENS].append(token)
                    
        return self[self.TOKENS]
        
    def get_types(self, lower=False):
        """
        @param lower: If set to True returns lowered types, otherwise
                      mixed-case types are the result.
        @return: A set of all types (=unique tokens) found in the
                 collection; types always get created again. Always 
                 create set once, both mixed- lower-cased.
        """
        # It's enough to check mixed-types 
        if len(self[self.TYPES]) == 0:
            for doc in self.get_docs():
                for token in doc.get_types(lower=False):
                    self[self.TYPES].add(token)
                for token in doc.get_types(lower=True):
                    self[self.TYPES_LOWERED].add(token)
        
        if (lower==False):
            return self[self.TYPES]
        # If lower==True
        return self[self.TYPES_LOWERED]
        
    def get_words(self, pos='_'):
        """
        Return all words, or a subset of them (for now: nouns).
        @param pos: Can be '_' (all words) or 'n' (nouns only).
        @return: Return words (look up document.py for more info how 
                 that comes). Do that once only.
        """
        if len(self[self.WORDS]) == 0:
            for doc in self.get_docs():
                for word in doc.get_words():
                    self[self.WORDS].append(word)
        
        # When nouns are required; XXX: (still) somewhat slow
        if (pos == 'n'):
            if len(self[self.NOUNS]) == 0:
                cnt = 0
                pb = ProgressBar(maxval=self[self.DOCS_COUNT]).start()
                for doc in self.get_docs():
                    cnt += 1; pb.update(cnt)
                    for noun in doc.get_words(pos='n',
                                ref_nouns=self[self.REF_NOUNS]):
                        self[self.NOUNS].append(noun)
                pb.finish()
                
                """ Alternative code to find the nouns over all
                    all the words, instead of a per-document basis.
                
                nouns_candidates = [nc for nc in self[self.WORDS] \
                            if not match("^[^a-zäöü]", nc) == None]
                for word in nouns_candidates:
                    cnt += 1
                    print str(cnt) + " of " + \
                        str(len(nouns_candidates))
                    if word in self[self.REF_NOUNS]:
                        self[self.NOUNS].append(word)
                """
            return self[self.NOUNS]
        
        # If pos is "_"
        return self[self.WORDS]
        
    def get_stems(self, uniq=False):
        """
        @param uniq: Defaults to False and indicates we want 
                     not-uniqe stems. Otherwise True can be used.
        @return: Set of all stems found in the documents.
        """
        var = self.STEMS
        if uniq == True:
            var = self.STEMS_UNIQ
        
        if len(self[var]) == 0:
            for doc in self.get_docs(): 
                for stem in doc.get_stems():
                    if uniq == True:
                        self[var].add(stem)
                    else:
                        self[var].append(stem)
            """
            Like this it was much more efficient (less method calls):    
            for word in self.get_words():
                self[self.STEMS].add(germanStemmer().stem(word))
            """
        return self[var]
           
    def get_freqdist(self):
        """
        @return: FreqDist object (of NLTK) allowing to get frequencies
        """
        if self[self.TEXT_FREQDIST] == None:
            self[self.TEXT_FREQDIST] = FreqDist(self.get_words())
            
        return self[self.TEXT_FREQDIST]
    
    def get_topwords(self, no_of_words=get_def_no_of_topwords()):
        """
        @param no_of_words: int indicating how many top words  (by
                              frequency) we want to gather; optional
        @return: Dictionary of top words along with its frequencies
        """
        if len(self[self.TOPWORDS]) == 0:
            self[self.TOPWORDS] = \
                self.get_freqdist().items()[:no_of_words]
        return self[self.TOPWORDS]
    
    def get_words_by_editdistance(self, editdistance,
        wordlen=get_def_len_for_editdistancing(),
        no_of_most_freq=get_def_no_of_topwords()):
        """
        @param editdistance: int indicating for which edit distance 
                             words should be checked
        @param wordlen: int indicating of which length source words
                        to be checked against (all) other words 
                        should be; optional
        @param no_of_most_freq: The (int) number of how many top words
                                 by frequency should be retrieved; 
                                 optional
        @return: A set with all pairs of words distanced by a certain
                 amount of edits (in some subset by the above 
                 parameters); this set is created once.
        """
        if len(self[self.WORDS_BY_EDITDISTANCE]) == 0:
            
            words_list = self.get_freqdist().keys()[:no_of_most_freq]
            ref_words_list = self.get_types()
            
            if not wordlen == 0:
                words_list = ListByLen(words_list)[wordlen:wordlen]
            
            words_listlen = len(words_list)
            print "Length of words list: " + str(words_listlen)
            cnt = 0
            for word1 in words_list:
                len_word1 = len(word1)
                start_len = len_word1 - editdistance
                end_len = len_word1 + editdistance
                ref_words_list = \
                    ListByLen(ref_words_list)[start_len:end_len]
                ref_word_listlen = len(ref_words_list)
                print "Length of reference words list: " + \
                    str(ref_word_listlen)
                cnt += 1
                print "Progress: " + str(float(cnt) /
                                         words_listlen * 100 ) + " %"
                for word2 in ref_words_list:
                    if edit_distance(word1, word2) == editdistance:
                        self[self.WORDS_BY_EDITDISTANCE].add((word1,
                                                                    word2))
                print "Number of forms found, up to now: " + \
                    str(len(self[self.WORDS_BY_EDITDISTANCE]))         
                    
        return self[self.WORDS_BY_EDITDISTANCE]
    
    #######################################################
    # Writer methods, i. e. methods to write files to disk.
    #######################################################
    
    def _write_raw(self):
        """
        Write raw text of <content> (of all mails) into a file, in the
        (alphabetical) order the files appear listed. Used internally.
        """
        f = open(get_raw_file(), "w", encoding=get_def_enc())
        f.write(self.get_text())
        f.close()
        
    def write_raw_text(self, in_one_file=False):
        """
        Write documents on a per-file basis in its raw content, or 
        write this content collectively in one file alone.
        XXX: Later replace write_raw() method above.
        @param in_one_file: If set to True writes all content in
                            one file
                            only, otherwise write every document in
                            its own file. Defaults to latter behaviour.
        """
        if in_one_file == True:
            self._write_raw()
        else:
            print "Write documents' raw content units line by line ..."
            for doc in self.get_docs():
                doc.write_content()
            print "... all " \
                + str(len(listdir(get_mailfolder(content_format="line")))) \
                + " documents written."
    
    def write_tokens(self):
        """
        Write all files' tokens into a file, as list, in the 
        appearing order.
        """
        f = open(get_tokens_file(), "w", encoding=get_def_enc())
        for token in self.get_tokens():
            f.write(token + "\n")
        f.close()
    
    def write_types(self, lower=False):
        """
        Write all files' types (=unique tokens) into a file, line by 
        line.
        @param lower: Optional parameter; default value here is False.
                      When set to True the types will all be printed
                      lower case, usually resulting in a smaller list.
        """
        f = open(get_types_file(lower), "w", encoding=get_def_enc())
        for t in self.get_types(lower):
            f.write(t + "\n")
        f.close()
    
    def write_words(self, pos='_'):
        """
        Write all words of all files into a file, one word per line, in
        the given order. Can also write only a subset of words.
        @param pos: Writes all words for value '_', and nouns for value
                    'n'.
        """
        f = open(get_words_file(pos=pos), "w", encoding=get_def_enc())      
        for token in self.get_words(pos=pos):
            f.write(token + "\n")
        f.close()
    
    def write_stems(self):
        """
        Write all (unique) stems into a file; one per line.
        """
        f = open(get_stems_file(), "w", encoding=get_def_enc())
        for stem in self.get_stems():
            f.write(stem + "\n")
        f.close()
        
    def write_topwords(self, no_of_words=get_def_no_of_topwords()):
        """
        Write the most frequent words into a file, ordered by
        descending frequency and with indication (seperated by three
        tabulators) of the absolute frequency number (in all documents
        of the collection).
        """
        filename = get_topwords_file()
        f = open(filename, "w", get_def_enc())
        for word, freq in self.get_topwords(no_of_words=no_of_words):
            f.write(word + "\t\t\t" + str(freq) + "\n")
        f.close()
   
    def write_words_by_editdistance(self,
        editdistance=get_def_editdistance_filename_suffix):
        """
        This method writes a file with sets of words distanced by a
        certain amount of edits, eventually adding a special suffix
        to the filename.
        @param: If (for distinguishing reasons) a special suffix should
                be appended to the default filename, this can be
                specified here as value of type str.
        """
        filename = get_words_by_editdistance_file(editdistance=editdistance)
        f = open(filename, "w", get_def_enc())
        for word1, word2 in self[self.WORDS_BY_EDITDISTANCE]:
            f.write(word1 + "\t" + word2 + "\n")
        f.close()
        print "File " + filename + " written to disk."