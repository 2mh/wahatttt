#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from os import makedirs
from os.path import getsize, exists, basename
from collections import defaultdict
from re import match
from codecs import open

from xml.etree import cElementTree as ET
from nltk import PunktWordTokenizer as tokenizer
from nltk.stem.snowball import GermanStemmer as germanStemmer
from hashlib import sha512

from library import normalize_word, rreplace, hashDict, clean_iterable
from settings import getMailFolder, getDefaultEncoding, getWordsFolder

class document(dict):
    """
    The class document is used to represent the individual documents,
    which are to be classified by wh4t.
    For the time being these documents are e-mail messages from the
    FTIUG debate@ mailing list.

    This class is a dict -- it parses the XML files and stores all of its 
    values in terms of key-value-pairs.
    """
    
    ############################################################
    # Attributes parsed
    # - The only (important) attributes used are mail id numbers
    #############################################################
    
    MAIL_TAG_ID_ATTR = "id"
    IN_REPLY_TO_TAG_ID_ATTR = MAIL_TAG_ID_ATTR
    
    #######################################################################
    # Tags parsed
    # - Tags used include such as <subj>, <author> or <content> (text body)
    #######################################################################

    MAIL_TAG = "mail" # containing id attrib
    URL_TAG = "url" # mail resource at http location, in HTML
    SUBJ_TAG = "subj"
    AUTHOR_TAG = "author"
    EMAIL_TAG = "email"
    DATE_TAG = "date" # saved in format: "%a, %d %b, %Y %H:%M:%S" (~ RFC2822)
    REF_TAG = "references"  # for <references> in <mail>, 
                            # containing <inReplyto>
    IN_REPLY_TO_TAG = "inReplyTo"
    CONTENT_TAG = "content"
    
    ##################################################################
    # Derived key-value pairs
    # - Derived pairs include tokenized text, stemmed text, words etc.
    ##################################################################
    
    TOKENS = "tokens"
    TYPES = "types"
    WORDS = "words"
    NOUNS = "nouns"
    STEMS = "stems"
    WORDS_BY_EDIT_DISTANCE = "words_by_edit_distance"
    TOP_WORDS = "top_words"
    TEXT_FREQ_DIST = "text_freq_dist"
    HASH_SUMS = "hashsums"
    
    #################################################################
    # Other key names, for now for storing the xml filename, and a
    # document id
    #################################################################
    
    XML_FILEPATH = "file"
    DOC_ID = "doc_id"
    
    ###################################
    # The object gets instantiated here
    ###################################
    
    def __init__(self, xmlFilePath):
        """
        @param xmlFilePath: The path to the xml file we want to parse
        Upon initialization all the tags and (important) attributes are
        read and stored in the object's itself (is a dict).
        """
        self[self.XML_FILEPATH] = xmlFilePath
        xmlFileHandler = ET.parse(xmlFilePath)
        
        # A document id, based on the (unique) file name
        self[self.DOC_ID] = rreplace(basename(self[self.XML_FILEPATH]),
                            ".xml", "", 1)
        
        # Populate self[self.HASH_SUMS] with hashsums
        self.loadHashsums()
        
        ################################################
        # Initialize items with material directly parsed
        #################################################
        
        # Get <mail> node
        xmlMailElem = xmlFileHandler.find(self.MAIL_TAG)
        
        # Store id attribute of <mail>
        self[self.MAIL_TAG] = xmlMailElem.get(self.MAIL_TAG_ID_ATTR)
   
        # Store text of <url> tag
        self[self.URL_TAG] = xmlMailElem.find(self.URL_TAG).text    
         
        # Store text of <subj> tag
        self[self.SUBJ_TAG] = xmlMailElem.find(self.SUBJ_TAG).text
        
        # Store text of <author> tag
        self[self.AUTHOR_TAG] = xmlMailElem.find(self.AUTHOR_TAG).text
        
        # Store text of <email> tag
        self[self.EMAIL_TAG] = xmlMailElem.find(self.EMAIL_TAG).text
        
        # Store text of <date> tag
        self[self.DATE_TAG] = xmlMailElem.find(self.DATE_TAG).text     
        
        # Get id from mail in <inReplyTo> tag, but:
        # - Not all mails have its parent: <references>
        # - However, thus who do have, do have -- ATM -- one reference only.
        xmlRefElem = xmlMailElem.find(self.REF_TAG)
        
        # Check for existence of <references>
        # At the end: Store id attribute of <inReplyToTag> in object 
        # itself, if the <references> tag does, in fact, exit.
        if (xmlRefElem) == None:
            self[self.IN_REPLY_TO_TAG] = None
        else:
            xmlInReplyToElem = \
            xmlMailElem.find(self.REF_TAG).find(self.IN_REPLY_TO_TAG)
        
            self[self.IN_REPLY_TO_TAG] = \
            xmlInReplyToElem.get(self.IN_REPLY_TO_TAG_ID_ATTR)
        
        # Store text of <content> tag (=mail body) 
        self[self.CONTENT_TAG] = \
            xmlFileHandler.find(self.CONTENT_TAG).text
            
        ###############################################################
        # Initialize items for later use, like tokens, words lists/sets
        ###############################################################
        
        # For holding tokens of the text
        self[self.TOKENS] = list()
    
        # For holding types (=unique tokens)
        self[self.TYPES] = set()
        
        # For holding words (=cleaned tokens)
        self[self.WORDS] = list()
        
        # The nouns (of the words)
        self[self.NOUNS] = list()
        
        # For holding (unique) stems
        self[self.STEMS] = set()
        
        # For holding pairs of words distanced by some edits, in a set
        self[self.WORDS_BY_EDIT_DISTANCE] = set()
        
        # For holding the most frequent words (with absolute frequency vals)
        self[self.TOP_WORDS] = defaultdict()
        
        # For holding an object to play with the frequency distribution
        self[self.TEXT_FREQ_DIST] = None
        
    ############################################################
    # Getters for the values stored in an instance of this class
    ############################################################
    
    def getId(self): 
        """
        @return: String with mail id
        """
        return self[self.MAIL_TAG]
    
    def getUrl(self): 
        """
        @return: String with url pointing to the web,
                 where the original mail (in HTML) can be found
        """
        return self[self.URL_TAG]
    
    def getSubj(self): 
        """
        @return: String with mail subject
        """
        return self[self.SUBJ_TAG]
    
    def getAuthor(self): 
        """
        @return: String with sender's name
        """
        return self[self.AUTHOR_TAG]
    
    def getEmail(self): 
        """
        @return: String with the e-mail address;
                 it may contain the name again
        """
        return self[self.EMAIL_TAG]
        
    def getDate(self): 
        """
        @return: String with the date in a standardized
                 notation
        """
        return self[self.DATE_TAG]
    
    def getInReplyToId(self): 
        """
        @return: String with mail id of the message this document
                 is referring to; caution: may be None, e. g. if
                 this document is the start of a thread and is thus
                 not in reply to another one
        """
        return self[self.IN_REPLY_TO_TAG] 
    
    def getRawContent(self): 
        """
        @return: String with the raw content -- as originally found
                 in <content>
        """
        return self[self.CONTENT_TAG]
    
    def getXmlFileName(self): 
        """
        @return: The full absolute path to the XML file represented
                 in this object.
        """
        return self[self.XML_FILEPATH]
    
    def getTokens(self):
        """
        @return: A list of all tokens found in the document; done by NLTK.
        """
        if len(self[self.TOKENS]) == 0:
            self[self.TOKENS] = tokenizer().tokenize(self.getRawContent())
        return self[self.TOKENS]
    
    def getTypes(self, lower=False):
        """
        @param lower: To be set to True to get only lower case types.
        @return: A set of all types (=unique tokens) found in the
                 document; create this set one time only.
        """
        if len(self[self.TYPES]) == 0:
            self[self.TYPES] = set(self.getTokens())
        if(lower == False):
            return self[self.TYPES]
        # Lower case list and return set
        return set(map(lambda x:x.lower(), self[self.TYPES]))
    
    def getWords(self, pos='_', reference_nouns=None):
        """
        @param pos: It's possible to say which words we want. ATM only '_'
                (all words; that's the default) or 'n' (nouns) are supported.
        @param reference_nouns: Optional parameter (together with pos) to
                               indicate which reference nouns (object nouns)
                               to use.
        @return: Return words (determined by surface forms) that seem to be 
                 of linguistic nature, and thus "real" words. Words in
                 this sense are built out of the tokens, which also include
                 lots of programming code in different languages or other
                 surfaces, which don't seem to be natural language -- like
                 PGP signatures or similar.
                 This construction is carried out one time only.
        XXX: This part my change heavily. Also: The regexps are ugly hacks.
        """
        doc_id = self[self.DOC_ID]
        hashsums_dict = self[self.HASH_SUMS]
        w, w_hash  = self.getFile(self.WORDS)
        folder = self.getFolderByKey(self.WORDS)      
         
        if self[self.HASH_SUMS] == 0 \
        or w_hash == None \
        or ''.join(hashsums_dict.keys()).find(folder + doc_id) < 0 \
        or not \
            w_hash == hashsums_dict[folder + doc_id]:
            
            nonWordSymbol = "0123456789<>=/"
            toAdd = True
            
            if len(self[self.WORDS]) == 0:  
                for t in self.getTokens():
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
                        self[self.WORDS].append(normalize_word(t))
                    else: # toAdd is False
                        toAdd = True
                self.writeFile(self.WORDS)
        else:
            self[self.WORDS] = clean_iterable(w)
        
        # By the very first run of the system a void hashsums file gets 
        # initialized.
        # After the above code, hashsums were created => let's reflect them.
        if len(self[self.HASH_SUMS]) == 0: self.loadHashsums()
            
        # Return only nouns; do it once only
        if pos == 'n' and not reference_nouns == None:
            # Approach by comparing against a nouns' list
            # and by considering words as nouns which start with
            # two upper case letters (being with high probability NEs).
            # XXX: May be possible to do faster.
            
            n, n_hash = self.getFile(self.NOUNS)
            folder = self.getFolderByKey(self.NOUNS)
                
            if n_hash == None \
            or ''.join(hashsums_dict.keys()).find(folder + doc_id) < 0 \
            or not n_hash == \
                hashsums_dict[folder + doc_id]:
                
                if len(self[self.NOUNS]) == 0:
                    noun_candidates = [nc for nc in self[self.WORDS] 
                                       if not match("^[^a-zäöü]", nc) == None]
                    for word in noun_candidates:
                        if word in reference_nouns \
                        or not match("^[A-Z]{2,}", word) == None:
                            self[self.NOUNS].append(word.strip())
                    self.writeFile(self.NOUNS)
            else:
                self[self.NOUNS] = clean_iterable(n)
                
            return self[self.NOUNS]
               
        # In case param pos is '_' (all words)            
        return self[self.WORDS]

    def getStems(self):
        """
        @return: Set of stems found upon the words. Create once.
        """
        if len(self[self.STEMS]) == 0:
            for word in self.getWords():
                self[self.STEMS].add(germanStemmer().stem(word))
        return self[self.STEMS]
    
    """
    WORDS_BY_EDIT_DISTANCE = "words_by_edit_distance"
    TOP_WORDS = "top_words"
    TEXT_FREQ_DIST = "text_freq_dist"
    """
    
    #################################################################
    # Other getters, not relying on data in an instance of this class
    #################################################################
    
    def getFileSize(self):
        """
        @return: Return integer with file size of the xml document
        """
        return getsize(self.getXmlFileName())
    
    def getRawLen(self): 
        """
        @return: Returns raw content as string, which originally 
                 was found in <content> node
        """
        return len(self.getRawContent())
    
    def getFile(self, key, hashsum=True):
        """
        @param key: Specifies which data to look at, e. g. "NOUNS" (str).
        @param hashsum: If True (default) return not only file's contents, but
                     also hashsum, otherwise return only file content.
        @return: Hashsum (str) of this document's data in some context
                 specified by param key. If no file available returns None
                 values.
        """
        sha512_sum = None
        content = None
        
        folder = self.getFolderByKey(key)
        try:
            f = open(folder + self[self.DOC_ID], "r", getDefaultEncoding())
            content = f.readlines()
            sha512_sum = sha512("".join(content)).hexdigest()
            f.close()
        except IOError:
            pass
        
        if hashsum == False:
            return content
        # Otherwise: Return a tuple
        return content, sha512_sum
    
    def getFolderByKey(self, key):
        """
        @param key: Key indicating which folder we want, e. g. "NOUNS"
        @return: str being folder path, based on a key value passed
        """
        folder = ""
        if key == self.WORDS:
            folder = getWordsFolder()
        elif key == self.NOUNS:
            folder = getWordsFolder(pos='n')
        # More folder variations to add
        return folder
    
    ##########################################
    # Methods to print content to the terminal
    ##########################################
    
    def printRawContent(self): 
        """
        Print the <content> part of the message to the terminal. 
        """        
        print self[self.CONTENT_TAG]
        
    ########################
    # Methods to write files
    ########################
    
    def writeFile(self, key, hashsum=True):
        """
        Writes a file (name: document name) to a specified folder.
        @param key: Specifies which data to write, based on the key of the
                    data stored in in this object, e. g. "WORDS" or "NOUNS".
        @param hashsum: Defaults to True and is used to write an hashsum of
                     the file to an hashfile.
        """
        folder = self.getFolderByKey(key)
        
        doc_id = self[self.DOC_ID]
        doc_as_str = "\n".join(self[key])
        sha512_sum = ""
        if (hashsum == True):
            hash_dict = hashDict() 
            sha512_sum = sha512(doc_as_str).hexdigest()
            hash_dict[folder + doc_id] = sha512_sum
            hash_dict.save()
        
        if not exists(folder): 
            print "Folder " + folder + " doesn't exist."
            try:
                makedirs(folder)
                print "Folder " + folder + " created."
            except Exception, e:
                print str(e)
        
        f = open(folder + doc_id, "w", getDefaultEncoding())
        f.write(doc_as_str)
        f.close()

    def writeContent(self, contentFormat="line", contentType="raw"):
        """
        Write files in different possible formats and content types to a 
        folder on disk.
        @param contentFormat: If "line" writes content unit line per line.
        @param contentType: If "raw", write tokens as is; other values like
                            "words" may (become) possible.
        """
        d = getMailFolder(contentFormat=contentFormat)
        if not exists(d):
            print "Folder " + d + " not availabe. Create it."
            makedirs(d)

        # For now only "raw" contentType exists, and "line" contentFormat
        f = open(d + self[self.DOC_ID], "w",
                 getDefaultEncoding())       
        for t in self.getTokens():
            f.write(t + "\n")
        f.close()
        
    ##############
    # Misc methods
    ##############
    def loadHashsums(self):
        """
        Simply read in the hashsumsfile (again) and save it here.
        This is important when changes occurred during processing.
        """
        self[self.HASH_SUMS] = hashDict()