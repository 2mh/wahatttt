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
from settings import getMailBodyWordsByEditDistanceFile
from settings import getMailBodyTopWordsFile
from document import document
from nltk import PunktWordTokenizer as tokenizer
from nltk.probability import FreqDist as freqdist
from nltk.stem.snowball import GermanStemmer as germanStemmer
from codecs import open
from sys import stdout
from re import match
from os import listdir
from nltk.metrics import edit_distance
from listByLen import listByLen
from collections import defaultdict

class collection:
    docList = []
    docsText = ""
    docsTokenized = []
    docsTyped = set() # unique elements
    docsWordsUnique = set() # unused
    docsWords = []
    docsStemmed = set()
    docsWordsByEditDistance = set()
    docsTopWords = defaultdict()
    
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
                self.docsStemmed.add(germanStemmer().stem(word))
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
    
    def getDocsTopWords(self,numberOfWords=42):
        if len(self.docsTopWords) == 0:
            self.docsTopWords = \
                self.docsTextFreqDist().items()[:numberOfWords]
        return self.docsTopWords
        
    def writeDocsTopWordsFile(self,numberOfWords=42):
        fileName = getMailBodyTopWordsFile()
        f = open(fileName,"w",getDefaultEncoding())
        for word,freq in self.getDocsTopWords(numberOfWords=numberOfWords):
            f.write(word + "\t\t" + str(freq) + "\n")
        f.close()
   
    def getWordsByEditDistance(self,editDistance,wordLen=None,numberOfMostFreq=1000):
        if len(self.docsWordsByEditDistance) == 0:
            
            wordsList = self.docsTextFreqDist().keys()[:numberOfMostFreq]
            referenceWordsList = self.getDocsTypes()
            
            if not wordLen == None:
                wordsList = listByLen(wordsList)[wordLen:wordLen]
            
            wordsListLen = len(wordsList)
            print "Length of words list: " + str(wordsListLen)
            cnt = 0
            for word1 in wordsList:
                lenWord1 = len(word1)
                startLen = lenWord1-editDistance
                endLen = lenWord1+editDistance
                referenceWordsList = listByLen(referenceWordsList)[startLen:endLen]
                referenceWordsListLen = len(referenceWordsList)
                print "Length of reference words list: " + \
                    str(referenceWordsListLen)
                cnt += 1
                print "Progress: " + str(float(cnt) / wordsListLen * 100 ) + " %"
                for word2 in referenceWordsList:
                    if edit_distance(word1,word2) == editDistance:
                        self.docsWordsByEditDistance.add((word1,word2))
                print "Number of forms found, up to now: " + \
                    str(len(self.docsWordsByEditDistance))                  
                    
        return self.docsWordsByEditDistance
   
    def writeWordsByEditDistanceFile(self,editDistance=""):
        fileName = getMailBodyWordsByEditDistanceFile(editDistance=editDistance)
        f = open(fileName,"w",getDefaultEncoding())
        for word1, word2 in self.docsWordsByEditDistance:
            f.write(word1 + "\t" + word2 + "\n")
        f.close()
        print "File " + fileName + " written to disk."