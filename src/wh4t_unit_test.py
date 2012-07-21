#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from wh4t.documents import collection
from wh4t.settings import printLine

# Program starts here
xmlDocuments = collection()
xmlDocument = xmlDocuments.getDoc(51) # Get a specific doc number for tests

# Print raw content, tokens and then types (mixed- and lowercase)
printLine()
print "Print raw content: "
print xmlDocument.getRawContent()
printLine()
print "Print tokens: "
print xmlDocument.getTokens()
printLine()
print "Print types (mixed-case): "
print xmlDocument.getTypes()
printLine()
print "Print types (lower-case): "
print xmlDocument.getTypes(lower=True)
printLine()
print "Print words: "
print xmlDocument.getWords()
printLine()
print "Print nouns: "
print xmlDocument.getWords(pos='n')
printLine()
print "Print stems: "
print xmlDocument.getStems()
printLine()