#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from wh4t.settings import printOwnInfo
from wh4t.documents import collection

printOwnInfo(__file__)

editDistance = 2
numberOfTopWords = 420
xmlCollection = collection()

"""XXX: Must be optimized first"""
print "Finding forms for the top " + str(numberOfTopWords) + " words by edit distance " + \
str(editDistance) + "; this may take a while!"
xmlCollection.getWordsByEditDistance(editDistance,numberOfMostFreq=numberOfTopWords)
xmlCollection.writeWordsByEditDistanceFile(editDistance=editDistance)
xmlCollection.writeDocsTopWordsFile(numberOfWords=numberOfTopWords)
print "Top words written to disk."