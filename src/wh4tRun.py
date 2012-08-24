#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from sys import stdout

from wh4t.settings import printOwnInfo
from wh4t.documents import collection
from wh4t.symbols import symbols

from nltk.text import TextCollection

printOwnInfo(__file__)

# Create a symbols object to see which symbols are available, along with
# their attributions
syms = symbols()
for sym, symClass in syms.items():
    print sym + "\t" + str(symClass)

# Params for getting (similar) words by edit distance and number of
# most frequent words (=top words) we are interested in.
editDistance = 1
numberOfTopWords = 420
xmlCollection = collection()
    
# For the above specified most frequent words search similar words (by
# edit distance) in the whole collection.
print "Finding forms for the top " + str(numberOfTopWords) + \
    " words by edit distance " + \
    str(editDistance) + "; this may take a while!"
xmlCollection.getWordsByEditDistance(editDistance,
                                     numberOfMostFreq=numberOfTopWords)

# Write the found sets to disk; also write most frequent words to disk.
xmlCollection.writeWordsByEditDistanceFile(editDistance=editDistance)
xmlCollection.writeDocsTopWordsFile(numberOfWords=numberOfTopWords)
print "Top words written to disk."

# XXX: BIG FUCK UP ################################## FIX FIX FIX #####

# Print idf, tf and tf-idf values for the term "CCC", in document
# no. 42 - for testing.
textCollection = TextCollection(xmlCollection.getDocsWords())
print "idf: " + str(textCollection.idf("CCC"))
print "tf: " + str(textCollection.tf("CCC", 
    TextCollection(xmlCollection.getDoc(42).getTokens())))
print "tf_idf: " + str(textCollection.tf_idf("CCC", 
    TextCollection(xmlCollection.getDoc(42).getTokens())))

# Do that now systematically for all documents
print "Document where tf is bigger 0:"
cnt = 0
for doc in xmlCollection.getDocs():
    tf = textCollection.tf("CCC", TextCollection(doc.getTokens()))
    stdout.write(str(tf) + ", ")
    cnt += 1
    if cnt == 10: 
        print
    cnt = 0
    if tf > 0.0: 
        print "\n" + doc.getXmlFileName()