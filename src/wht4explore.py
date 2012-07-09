#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from wht4.settings import printOwnInfo
from wht4.settings import getMailBodyRawFile
from wht4.documents import collection
from wht4.settings import getMailBodySymbolsFile
from wht4.settings import printOK
from wht4.symbols import symbols
from sys import stdout
from wht4.settings import getMailBodyTokensFile
from wht4.settings import getMailBodyTypesFile
from wht4.settings import getMailBodyWordsFile
from wht4.settings import print72 as prL

printOwnInfo(__file__)       
        
# Program starts here
xmlCollection = collection()
print "-- Calculating total file size ..."
print "Total file size: " + str(xmlCollection.getDocsFileSize()) + " bytes"
prL()
print "-- Calculating raw size of text ..."
print "Total raw size: " + str(xmlCollection.getDocsRawSize()) + " bytes"
stdout.write("Write raw text into file: " + getMailBodyRawFile())
xmlCollection.writeDocsRawFile(); printOK()
stdout.write("Write symbols used into file: " + getMailBodySymbolsFile())
syms = symbols()
syms.writeSymbolsFile(); printOK(); prL()
print "-- Get unique symbols ..."
print "Total number of unique symbols: " + str(syms.getNumberOfSymbols())
prL()
print "-- Get tokens ...";
tokenizedText = xmlCollection.getDocsTokens()
print "Total number of (raw) tokens: " + \
str(len(tokenizedText))
prL()
print "-- Get types ..."
typedText = xmlCollection.getDocsTypes()
typedTextLowered = xmlCollection.getDocsTypes(lower=True)
print "Total number of (raw) types: " + \
str(len(typedText))
print "Total number of (raw) types (lower-cased): " + \
str(len(typedTextLowered))
prL()
print "-- Get number of words ..."
words = xmlCollection.getDocsWords()
print "Total number of words: " + \
str(len(words))
prL()
print "-- Get number of stems ...";
stemmedText = xmlCollection.getDocsStems()
print "Total number of stems: " + \
str(len(stemmedText))
prL()
stdout.write("Write tokens into file: " + getMailBodyTokensFile())
xmlCollection.writeDocsTokenFile(); printOK()
stdout.write("Write types into file: " + getMailBodyTypesFile())
xmlCollection.writeDocsTypesFile(); printOK()
stdout.write("Write types (lowered) into file: " + getMailBodyTypesFile(lower=True))
xmlCollection.writeDocsTypesFile(lower=True); printOK()
stdout.write("Write words into file: " + getMailBodyWordsFile())
xmlCollection.writeDocsWordsFile(); printOK()
prL()
print "Top 10 words: "
for stem in xmlCollection.docsTextFreqDist().keys()[:10]: print stem
prL()
