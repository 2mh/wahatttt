#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from settings import getMailFolder
from settings import getMailBodyTokensFile
from settings import getDefaultEncoding
from settings import getMailBodyTypesFile
from settings import getMailBodyRawFile
from settings import getMailBodyWordsFile
from settings import getMailBodyStemsFile
from document import document
from nltk import PunktWordTokenizer as tokenizer
from nltk.probability import FreqDist as freqdist
from nltk.stem.snowball import GermanStemmer as germanStemmer
from codecs import open
from sys import stdout
from re import match
from os import listdir

class collection:
    docList = []
    docsText = ""
    docsTokenized = []
    docsTyped = set() # unique elements
    docsWordsUnique = set() # unused
    docsWords = []
    docsStemmed = []
    
    docsTextFreqDistObj = None
    
    def __init__(self):
        for xmlFileName in listdir(getMailFolder()):
            xmlDocument = document(getMailFolder()+xmlFileName)
            self.docList.append(xmlDocument)
    
    def addDoc(self,doc):
        self.docList.append(doc)
        
    def getDoc(self,pos): return self.docList[pos]
    
    def getDocs(self): return self.docList
    
    def writeDocsRawFile(self):
        f = open(getMailBodyRawFile(),"w",encoding=getDefaultEncoding())
        f.write(self.getDocsText())
        f.close()
    
    def getDocsFileSize(self):
        folderTotalSize = 0
        for doc in self.docList:
            folderTotalSize += doc.getFileSize()
        return folderTotalSize
    
    def getDocsRawSize(self):
        folderNetSize = 0
        for doc in self.docList:
            folderNetSize += doc.getRawLen()
        return folderNetSize
    
    def getDocsText(self):
        # Only do it, if not already done
        if len(self.docsText) == 0:
            for doc in self.getDocs():
                self.docsText += doc.getRawContent()
        
        return self.docsText
    
    def printDocsText(self): print self.getDocsText()
    
    def getDocsTokens(self):
        # Only do it once
        if len(self.docsTokenized) == 0:
            self.docsTokenized = tokenizer().tokenize(self.getDocsText())
        return self.docsTokenized
    
    def writeDocsTokenFile(self):
        f = open(getMailBodyTokensFile(),"w",encoding=getDefaultEncoding())
        
        for token in self.getDocsTokens():
            f.write(token+"\n")
        
        f.close()  
        
    def printDocsTokenFile(self):
        f = open(getMailBodyTokensFile(),"r")
        
        for line in f.readlines():
            stdout.write(line)
        
        f.close()
        
    def getDocsTypes(self,lower=False):
        # Only ``setisfy'' once
        if len(self.docsTyped) == 0:
            self.docsTyped = set(self.getDocsTokens())
        if(lower == False):
            return self.docsTyped
        # lowercase list and make set
        return set(map(lambda x:x.lower(), self.docsTyped))
    
    def writeDocsTypesFile(self,lower=False):
        
        f = open(getMailBodyTypesFile(lower),"w",encoding=getDefaultEncoding())
        
        for t in self.getDocsTypes(lower):
            f.write(t+"\n")
        
        f.close()
        
    def getDocsWords(self):
        nonWordSymbol = "0123456789<>=/"
        toAdd = True
        
        if len(self.docsWords) == 0:
            
            for t in self.getDocsTokens():
                for s in nonWordSymbol:
                    if s in t:
                        toAdd = False
                        break
                if not match("[a-z]+\.[a-z]+",t) == None \
                or not match("[ \*_\]\^\\\\!$\"\'%` ]+.*",t) == None \
                or not match("[ &*\(\)+\#,-.:;?+\\@\[ ]+.*",t) == None \
                or not match("[a-z]{1}-",t) == None \
                or t.find("--") >= 0 or t.find("..") >= 0:
                    toAdd = False             
                if (toAdd == True):    
                    self.docsWords.append(t)
                else: # toAdd is False
                    toAdd = True
        
        return self.docsWords
    
    def writeDocsWordsFile(self):
        f = open(getMailBodyWordsFile(),"w",encoding=getDefaultEncoding())
        
        for token in self.getDocsWords():
            f.write(token+"\n")
        
        f.close()
        
    def getDocsStems(self):
        if len(self.docsStemmed) == 0:
            for word in self.getDocsWords():
                self.docsStemmed.append(germanStemmer().stem(word))
        return self.docsStemmed
    
    def writeStemsFile(self):
        f = open(getMailBodyStemsFile(),"w",encoding=getDefaultEncoding())
        
        for stem in self.getDocsStems():
            f.write(stem+"\n")
            
        f.close()
           
    def docsTextFreqDist(self):
        if self.docsTextFreqDistObj == None:
            self.docsTextFreqDistObj = freqdist(self.getDocsWords())
            
        return self.docsTextFreqDistObj
    
