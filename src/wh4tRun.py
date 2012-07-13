#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from wh4t.settings import printOwnInfo
from wh4t.documents import collection

printOwnInfo(__file__)

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