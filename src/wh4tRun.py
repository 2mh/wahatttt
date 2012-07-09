#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from wh4t.settings import printOwnInfo
from wh4t.documents import collection

printOwnInfo(__file__)

dist = 2
noOfTopWords = 23000
xmlCollection = collection()

"""XXX: Must be optimized first"""
print "Finding forms for the top " + str(noOfTopWords) + " words by edit distance " + \
str(dist) + "; this may take a while!"
xmlCollection.getWordsByEditDistance(dist,numberOfMostFreq=noOfTopWords)
xmlCollection.writeWordsFileByEditDistance(distance=dist)