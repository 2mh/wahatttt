#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open
from os import listdir
from collections import defaultdict

from nltk.probability import FreqDist as freqdist
from nltk.metrics import edit_distance
from progressbar import ProgressBar as progressbar

from document import document
from listByLen import listByLen
from settings import getMailFolder, getMailBodyTokensFile, \
                     getDefaultEncoding, getMailBodyTypesFile, \
                     getMailBodyRawFile, getMailBodyWordsFile, \
                     getMailBodyStemsFile, \
                     getMailBodyWordsByEditDistanceFile, \
                     getMailBodyTopWordsFile, getDefaultNumberOfTopWords, \
                     getDefaultSourceWordLenForEditDistancing, \
                     getDefaultEditDistanceFilenameSuffix
from nouns import nouns

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
    DOCS_TYPED_LOWERED = "docs_typed_lowered"
    DOCS_WORDS = "docs_words"
    DOCS_STEMMED = "docs_stemmed"
    DOCS_WORDS_BY_EDIT_DISTANCE = "docs_words_by_edit_distance"
    DOCS_TOP_WORDS = "docs_top_words"
    DOCS_TEXT_FREQ_DIST = "docs_text_freq_dist"    
    DOCS_NOUNS = "docs_nouns"
    DOCS_REF_NOUNS = "docs_ref_nouns" 
    DOCS_NUMBER = "docs_number"
        
    def __init__(self):
        """
        Initialization of key-value pairs to hold the collection
        of documents.
        """
        dict.__init__(self)
        
        # For holding a list of documents
        self.__setitem__(self.DOC_LIST, list())

        # For holding the collection's raw text
        self.__setitem__(self.DOCS_TEXT, str())
        
        # For holding all of the text tokenized by NLTK
        self.__setitem__(self.DOCS_TOKENIZED, list())
        
        # For holding the types of the collection
        self.__setitem__(self.DOCS_TYPED, set())
        
        # For holding the lowered types of the collection
        self.__setitem__(self.DOCS_TYPED_LOWERED, set())
        
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
        
        # To hold all nouns found, in a list (for frequency analysis)
        self.__setitem__(self.DOCS_NOUNS, list())
        
        # Initializes a nouns object (is a list) of reference nouns we use 
        # to find nouns in the collection
        self.__setitem__(self.DOCS_REF_NOUNS, nouns())
        
        # Read in all documents
        # XXX: This part may change in its behaviour soon
        filesList = listdir(getMailFolder())
        for xmlFileName in filesList:
            xmlDocument = document(getMailFolder() + xmlFileName)
            self[self.DOC_LIST].append(xmlDocument)
            
        # Store number of files found
        self.__setitem__(self.DOCS_NUMBER, len(filesList))
        
    def getDoc(self, pos): 
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
            for doc in self.getDocs():
                for token in doc.getTokens():
                    self[self.DOCS_TOKENIZED].append(token)
                    
        return self[self.DOCS_TOKENIZED]
        
    def getDocsTypes(self, lower=False):
        """
        @param lower: If set to True returns lowered types, otherwise
                      mixed-case types are the result.
        @return: A set of all types (=unique tokens) found in the
                 collection; types always get created again. Always create
                 set once, both mixed- lower-cased.
        """
        # It's enough to check mixed-types 
        if len(self[self.DOCS_TYPED]) == 0:
            for doc in self.getDocs():
                for token in doc.getTypes(lower=False):
                    self[self.DOCS_TYPED].add(token)
                for token in doc.getTypes(lower=True):
                    self[self.DOCS_TYPED_LOWERED].add(token)
        
        if (lower==False):
            return self[self.DOCS_TYPED]
        # If lower==True
        return self[self.DOCS_TYPED_LOWERED]
        
    def getDocsWords(self, pos='_'):
        """
        Return all words, or a subset of them (for now: nouns).
        @param pos: Can be '_' (all words) or 'n' (nouns only).
        @return: Return words (look up document.py for more info how that
                 comes). Do that once only.
        """
        if len(self[self.DOCS_WORDS]) == 0:
            for doc in self.getDocs():
                for word in doc.getWords():
                    self[self.DOCS_WORDS].append(word)
        
        # When nouns are required; XXX: (still) somewhat slow
        if (pos == 'n'):
            if len(self[self.DOCS_NOUNS]) == 0:
                cnt = 0
                pb = progressbar(maxval=self[self.DOCS_NUMBER]).start()
                for doc in self.getDocs():
                    cnt += 1; pb.update(cnt)
                    for noun in doc.getWords(pos='n',
                                reference_nouns=self[self.DOCS_REF_NOUNS]):
                        self[self.DOCS_NOUNS].append(noun)
                pb.finish()
                
                """ Alternative code to find the nouns over all
                    all the words, instead of a per-document basis.
                
                nouns_candidates = [nc for nc in self[self.DOCS_WORDS] \
                            if not match("^[^a-zäöü]", nc) == None]
                for word in nouns_candidates:
                    cnt += 1
                    print str(cnt) + " of " + str(len(nouns_candidates))
                    if word in self[self.DOCS_REF_NOUNS]:
                        self[self.DOCS_NOUNS].append(word)
                """
            return self[self.DOCS_NOUNS]
        
        # If pos is "_"
        return self[self.DOCS_WORDS]
        
    def getDocsStems(self):
        """
        @return: Set of all stems found in the documents.
        """
        if len(self[self.DOCS_STEMMED]) == 0:
            for doc in self.getDocs(): 
                for stem in doc.getStems():
                    self[self.DOCS_STEMMED].add(stem)
            """
            Like this it was much more efficient (less method calls):    
            for word in self.getDocsWords():
                self[self.DOCS_STEMMED].add(germanStemmer().stem(word))
            """
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
        
    def writeRawText(self, in_one_file=False):
        """
        Write documents on a per-file basis in its raw content, or 
        write this content collectively in one file alone.
        XXX: Later replace writeDocsRawFile() method above.
        @param in_one_file: If set to True writes all content in one file
                            only, otherwise write every document in its own
                            file. Defaults to latter behaviour.
        """
        if in_one_file == True:
            self.writeDocsRawFile()
        else:
            print "Write documents' raw content units line by line ..."
            for doc in self.getDocs():
                doc.writeContent()
            print "... all " \
                + str(len(listdir(getMailFolder(contentFormat="line")))) \
                + " documents written."
    
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
    
    def writeDocsWordsFile(self, pos='_'):
        """
        Write all words of all files into a file, one word per line, in
        the given order. Can also write only a subset of words.
        @param pos: Writes all words for value '_', and nouns for value 'n'.
        """
        f = open(getMailBodyWordsFile(pos=pos), "w", 
                 encoding=getDefaultEncoding())      
        for token in self.getDocsWords(pos=pos):
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
        for word, freq in self.getDocsTopWords(numberOfWords=numberOfWords):
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