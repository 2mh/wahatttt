#! /usr/bin/env python2.7
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
from progressbar import ProgressBar

from wh4t.documents import Collection
from wh4t.nouns import Nouns
from wh4t.settings import print_line, get_stems_file, get_def_enc, \
                          print_own_info

def main():
    """
    From here a linguistic classifier should emerge that classifies
    the documents upon the nouns employed.
    XXX: Work-in-progress
    """
    print_own_info(__file__)
    
    """    
    xmldocs = Collection()
    all_words_list = xmldocs.get_words()
    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(all_words_list)
    for pair in finder.nbest(bigram_measures.pmi, 50): print pair
    
    for doc in xmldocs:
        nounslist = doc.get_words(pos="n",ref_nouns=Nouns())
        finder = BigramCollocationFinder.from_words(nounslist)
        nounsfreq = FreqDist(nounslist).items()
        print nounslist
        print doc.get_xml_filename()
        print nounsfreq
        print finder.nbest(bigram_measures.pmi, 5)
        print_line()
    """
    
if __name__ == "__main__":
    main()