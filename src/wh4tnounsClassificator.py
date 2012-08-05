#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from nltk.probability import FreqDist
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import BigramAssocMeasures
from nltk.text import Text
from nltk.text import TextCollection
from progressbar import ProgressBar as progressbar

from wh4t.documents import collection
from wh4t.nouns import nouns
from wh4t.settings import printLine

def main():
    """
    From here a linguistic classifier should emerge that classifies
    the documents upon the nouns employed.
    XXX: Work-in-progress
    """

    xmlCollection = collection()
    nltkTextCollectionList = list()
    
    print "Creating NLTK text collection ... "
    xmlCollectionList = xmlCollection.getDocs()
    pb = progressbar(maxval=len(xmlCollectionList)).start()
    cnt = 0
    for doc in xmlCollectionList:
        cnt += 1
        pb.update(cnt)
        nltkTextCollectionList.append(doc.getWords(pos='n',
                                                   reference_nouns=nouns()))
    nltkTextCollection = TextCollection(nltkTextCollectionList)
    
    print "Calculating idf values for all words ..."
    allWords = xmlCollection.getDocsWords(pos='n')
    idfList = list()
    pb = progressbar(maxval=len(allWords)).start()
    cnt = 0
    for word in allWords:
        cnt += 1
        pb.update(cnt)
        idf = nltkTextCollection.idf(word)
        if idf > 0.0: 
            idfList.append((idf, word))
    
    for pair in idfList: 
        print pair
        
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