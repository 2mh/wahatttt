#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open
from re import match
from os import listdir
from collections import defaultdict

from nltk import PunktWordTokenizer as tokenizer
from nltk.probability import FreqDist as freqdist
from nltk.stem.snowball import GermanStemmer as germanStemmer
from nltk.metrics import edit_distance

from document import document
from listByLen import listByLen
from settings import getMailFolder
from settings import getMailBodyTokensFile
from settings import getDefaultEncoding
from settings import getMailBodyTypesFile
from settings import getMailBodyRawFile
from settings import getMailBodyWordsFile
from settings import getMailBodyStemsFile
from settings import getMailBodyWordsByEditDistanceFile
from settings import getMailBodyTopWordsFile
from settings import getDefaultNumberOfTopWords
from settings import getDefaultSourceWordLenForEditDistancing
from settings import getDefaultEditDistanceFilenameSuffix

class collection(dict):
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
    DOCS_TEXT = "docs_text"
    DOCS_TOKENIZED = "docs_tokenized"
    DOCS_TYPED = "docs_typed"
    DOCS_WORDS = "docs_words"
    DOCS_STEMMED = "docs_stemmed"
    DOCS_WORDS_BY_EDIT_DISTANCE = "docs_words_by_edit_distance"
    DOCS_TOP_WORDS = "docs_top_words"
    DOCS_TEXT_FREQ_DIST = "docs_text_freq_dist"    
        
    def __init__(self):
        """
        Initialization of key-value pairs to hold the collection
        of documents.
        """
        
        # For holding a list of documents
        self.__setitem__(self.DOC_LIST, list())

        # For holding the collection's raw text
        self.__setitem__(self.DOCS_TEXT, str())
        
        # For holding all of the text tokenized by NLTK
        self.__setitem__(self.DOCS_TOKENIZED, list())
        
        # For holding the types of the collection
        self.__setitem__(self.DOCS_TYPED, set())
        
        # For holding a list of all the words, i. e. the cleaned
        # tokens; the words are not necessarily unique 
        self.__setitem__(self.DOCS_WORDS, list())
        
        # For holding a list of all the stems; it's a set (=> unique values)
        self.__setitem__(self.DOCS_STEMMED, set())
        
        # For holding unique pairs of words being of some edit distance
        self.__setitem__(self.DOCS_WORDS_BY_EDIT_DISTANCE, set())
        
        # For holding a specified amount of most frequent words, along
        # with each frequency as absolute number.
        self.__setitem__(self.DOCS_TOP_WORDS, defaultdict())
        
        # To hold an object with the frequencies of all words
        self.__setitem__(self.DOCS_TEXT_FREQ_DIST, None)
        
        # Read in all documents
        # XXX: This part may change in its behaviour soon
        for xmlFileName in listdir(getMailFolder()):
            xmlDocument = document(getMailFolder() + xmlFileName)
            self[self.DOC_LIST].append(xmlDocument)
        
    def getDoc(self,pos): 
        """
        @param pos: The position (int) of the document in the list.
        @return: A specific document (of type document)
        """
        return self[self.DOC_LIST][pos]
    
    def getDocs(self): 
        """
        @return: List of all documents in this collection
        """
        return self[self.DOC_LIST]
    
    def getDocsFileSize(self):
        """
        @return: Size of all files (in bytes) of the collection, including
                all (meta) data
        """
        folderTotalSize = 0
        for doc in self.getDocs():
            folderTotalSize += doc.getFileSize()
        return folderTotalSize
    
    def getDocsRawSize(self):
        """
        @return: Size of only the body content parts of the collection
        """
        folderNetSize = 0
        for doc in self.getDocs():
            folderNetSize += doc.getRawLen()
        return folderNetSize
    
    def getDocsText(self):
        """
        @return: Return as a string all the documents' body content, in
                 the given raw form; do the retrieval only once
        """
        if len(self[self.DOCS_TEXT]) == 0:
            for doc in self.getDocs():
                self[self.DOCS_TEXT] += doc.getRawContent()      
        return self[self.DOCS_TEXT]
    
    def getDocsTokens(self):
        """
        @return: A list of all tokens found in the collection and ordered
                 as is. Ensure to get the tokens once only.
        """
        if len(self[self.DOCS_TOKENIZED]) == 0:
            self[self.DOCS_TOKENIZED] = \
                tokenizer().tokenize(self.getDocsText())
        return self[self.DOCS_TOKENIZED]
        
    def getDocsTypes(self, lower=False):
        """
        @return: A set of all types (=unique tokens) found in the
                 collection; create this set one time only.
        """
        if len(self[self.DOCS_TYPED]) == 0:
            self[self.DOCS_TYPED] = set(self.getDocsTokens())
        if(lower == False):
            return self[self.DOCS_TYPED]
        # Lower case list and return set
        return set(map(lambda x:x.lower(), self[self.DOCS_TYPED]))
        
    def getDocsWords(self):
        """
        @return: Return words (determined by surface forms) that seem to be 
                 of linguistic nature, and thus "real" words. Words in
                 this sense are built out of the tokens, which also include
                 lots of programming code in different languages or other
                 surfaces, which don't seem to be natural language -- like
                 PGP signatures or similar.
                 This construction is carried out one time only.
        XXX: This part my change heavily. Also: The regexps are ugly hacks.
        """
        nonWordSymbol = "0123456789<>=/"
        toAdd = True
        
        if len(self[self.DOCS_WORDS]) == 0:  
            for t in self.getDocsTokens():
                for s in nonWordSymbol:
                    if s in t:
                        toAdd = False
                        break
                if not match("[a-z]+\.[a-z]+", t) == None \
                or not match("[ \*_\]\^\\\\!$\"\'%` ]+.*", t) == None \
                or not match("[ &*\(\)+\#,-.:;?+\\@\[ ]+.*", t) == None \
                or not match("[a-z]{1}-", t) == None \
                or t.find("--") >= 0 or t.find("..") >= 0:
                    toAdd = False             
                if (toAdd == True):    
                    self[self.DOCS_WORDS].append(t)
                else: # toAdd is False
                    toAdd = True
        
        return self[self.DOCS_WORDS]
        
    def getDocsStems(self):
        """
        @return: Set of stems found upon the words. Create once.
        """
        if len(self[self.DOCS_STEMMED]) == 0:
            for word in self.getDocsWords():
                self[self.DOCS_STEMMED].add(germanStemmer().stem(word))
        return self[self.DOCS_STEMMED]
           
    def docsTextFreqDist(self):
        """
        @return: FreqDist object (of NLTK) allowing to get frequencies
        """
        if self[self.DOCS_TEXT_FREQ_DIST] == None:
            self[self.DOCS_TEXT_FREQ_DIST] = freqdist(self.getDocsWords())
            
        return self[self.DOCS_TEXT_FREQ_DIST]
    
    def getDocsTopWords(self, numberOfWords=getDefaultNumberOfTopWords()):
        """
        @param numberOfWords: int indicating how many top words 
                              (by frequency) we want to gather; optional
        @return: Dictionary of top words along with its frequencies 
        """
        if len(self[self.DOCS_TOP_WORDS]) == 0:
            self[self.DOCS_TOP_WORDS] = \
                self.docsTextFreqDist().items()[:numberOfWords]
        return self[self.DOCS_TOP_WORDS]
    
    def getWordsByEditDistance(self, editDistance,
        wordLen=getDefaultSourceWordLenForEditDistancing(),
        numberOfMostFreq=getDefaultNumberOfTopWords):
        """
        @param editDistance: int indicating for which edit distance words
                             should be checked
        @param wordLen: int indicating of which length source words to be
                        checked against (all) other words should be; optional
        @param numberOfMostFreq: The (int) number of how many top words
                                 by frequency should be retrieved; optional
        @return: A set with all pairs of words distanced by a certain amount
                 of edits (in some subset by the above parameters); this
                 set is created once.
        """
        if len(self[self.DOCS_WORDS_BY_EDIT_DISTANCE]) == 0:
            
            wordsList = self.docsTextFreqDist().keys()[:numberOfMostFreq]
            referenceWordsList = self.getDocsTypes()
            
            if not wordLen == 0:
                wordsList = listByLen(wordsList)[wordLen:wordLen]
            
            wordsListLen = len(wordsList)
            print "Length of words list: " + str(wordsListLen)
            cnt = 0
            for word1 in wordsList:
                lenWord1 = len(word1)
                startLen = lenWord1 - editDistance
                endLen = lenWord1 + editDistance
                referenceWordsList = \
                    listByLen(referenceWordsList)[startLen:endLen]
                referenceWordsListLen = len(referenceWordsList)
                print "Length of reference words list: " + \
                    str(referenceWordsListLen)
                cnt += 1
                print "Progress: " + str(float(cnt) / wordsListLen * 100 ) \
                 + " %"
                for word2 in referenceWordsList:
                    if edit_distance(word1, word2) == editDistance:
                        self[self.DOCS_WORDS_BY_EDIT_DISTANCE].add((word1,
                                                                    word2))
                print "Number of forms found, up to now: " + \
                    str(len(self[self.DOCS_WORDS_BY_EDIT_DISTANCE]))                  
                    
        return self[self.DOCS_WORDS_BY_EDIT_DISTANCE]
    
    #######################################################
    # Writer methods, i. e. methods to write files to disk.
    #######################################################
    
    def writeDocsRawFile(self):
        """
        Write raw text of <content> (of all mails) into a file, in the
        (alphabetical) order the files appear listed.
        """
        f = open(getMailBodyRawFile(), "w", encoding=getDefaultEncoding())
        f.write(self.getDocsText())
        f.close()
    
    def writeDocsTokenFile(self):
        """
        Write all files' tokens into a file, as list, in the appearing order.
        """
        f = open(getMailBodyTokensFile(), "w", encoding=getDefaultEncoding())       
        for token in self.getDocsTokens():
            f.write(token + "\n")
        f.close()
    
    def writeDocsTypesFile(self, lower=False):
        """
        Write all files' types (=unique tokens) into a file, line by line.
        @param lower: Optional parameter; default value here is False. When
                      set to True the types will all be printed lower case,
                      usually resulting in a smaller list.
        """
        f = open(getMailBodyTypesFile(lower), "w",
                 encoding=getDefaultEncoding())
        for t in self.getDocsTypes(lower):
            f.write(t + "\n")
        f.close()
    
    def writeDocsWordsFile(self):
        """
        Write all words of all files into a file, one word per line, in
        the given order.
        """
        f = open(getMailBodyWordsFile(), "w", encoding=getDefaultEncoding())      
        for token in self.getDocsWords():
            f.write(token + "\n")
        f.close()
    
    def writeStemsFile(self):
        """
        Write all (unique) stems into a file; one per line.
        """
        f = open(getMailBodyStemsFile(), "w", encoding=getDefaultEncoding())
        for stem in self.getDocsStems():
            f.write(stem + "\n")
        f.close()
        
    def writeDocsTopWordsFile(self,
                              numberOfWords=getDefaultNumberOfTopWords()):
        """
        Write the most frequent words into a file, ordered by descending
        frequency and with indication (seperated by three tabulators) of
        the absolute frequency number (in all documents of the collection).
        """
        fileName = getMailBodyTopWordsFile()
        f = open(fileName, "w", getDefaultEncoding())
        for word,freq in self.getDocsTopWords(numberOfWords=numberOfWords):
            f.write(word + "\t\t\t" + str(freq) + "\n")
        f.close()
   
    def writeWordsByEditDistanceFile(self,
        editDistance=getDefaultEditDistanceFilenameSuffix):
        """
        This method writes a file with sets of words distanced by a certain
        amount of edits, eventually adding a special suffix to the filename.
        @param: If (for distinguishing reasons) a special suffix should
                be appended to the default filename, this can be specified
                here as value of type str.
        """
        fileName = \
            getMailBodyWordsByEditDistanceFile(editDistance=editDistance)
        f = open(fileName, "w", getDefaultEncoding())
        for word1, word2 in self[self.DOCS_WORDS_BY_EDIT_DISTANCE]:
            f.write(word1 + "\t" + word2 + "\n")
        f.close()
        print "File " + fileName + " written to disk."