#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from codecs import open

from nltk.probability import FreqDist
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import BigramAssocMeasures
from nltk.text import Text
from nltk.text import TextCollection
from progressbar import ProgressBar as progressbar

from wh4t.documents import collection
from wh4t.nouns import nouns
from wh4t.settings import printLine
from wh4t.settings import getMailBodyStemsFile, getDefaultEncoding

def main():
    """
    From here a linguistic classifier should emerge that classifies
    the documents upon the nouns employed.
    XXX: Work-in-progress
    """
        
    """
    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(allWordsList)
    for pair in finder.nbest(bigram_measures.pmi, 50): print pair
    
    for doc in xmlDocsList:
        nounsList = doc.getWords(pos="n",reference_nouns=nouns())
        finder = BigramCollocationFinder.from_words(nounsList)
        nounsFreq = FreqDist(nounsList).items()
        print nounsList
        print doc.getXmlFileName()
        print nounsFreq
        print finder.nbest(bigram_measures.pmi, 5)
        printLine()
    """
    
if __name__ == "__main__":
    main()