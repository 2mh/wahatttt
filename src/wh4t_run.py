#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from sys import stdout

from wh4t.library import print_own_info
from wh4t.documents import Collection
from wh4t.symbols import Symbols

from nltk.text import TextCollection

print_own_info(__file__)

# Create a symbols object to see which symbols are available, along with
# their attributions
symbols = Symbols()
for sym, sym_class in symbols.items():
    print sym + "\t" + str(sym_class)

# Params for getting (similar) words by edit distance and number of
# most frequent words (=top words) we are interested in.
editdistance = 1
no_of_topwords = 420
xmlcollection = Collection()
    
# For the above specified most frequent words search similar words (by
# edit distance) in the whole collection.
print "Finding forms for the top " + str(no_of_topwords) + \
    " words by edit distance " + \
    str(editdistance) + "; this may take a while!"
xmlcollection.get_words_by_editdistance(editdistance=editdistance,
                                        no_of_most_freq=no_of_topwords)

# Write the found sets to disk; also write most frequent words to disk.
xmlcollection.write_words_by_editdistance(editdistance=editdistance)
xmlcollection.write_topwords(no_of_words=no_of_topwords)
print "Top words written to disk."

# XXX: BIG FUCK UP ################################## FIX FIX FIX #####

# Print idf, tf and tf-idf values for the term "CCC", in document
# no. 42 - for testing.
nltk_textcollection = TextCollection(xmlcollection.get_words())
print "idf: " + str(nltk_textcollection.idf("CCC"))
print "tf: " + str(nltk_textcollection.tf("CCC", 
    TextCollection(xmlcollection.get_doc(42).get_tokens())))
print "tf_idf: " + str(nltk_textcollection.tf_idf("CCC", 
    TextCollection(xmlcollection.get_doc(42).get_tokens())))

# Do that now systematically for all documents
print "Document where tf is bigger 0:"
cnt = 0
for doc in xmlcollection.get_docs():
    tf = nltk_textcollection.tf("CCC", TextCollection(doc.get_tokens()))
    stdout.write(str(tf) + ", ")
    cnt += 1
    if cnt == 10: 
        print
    cnt = 0
    if tf > 0.0: 
        print "\n" + doc.get_xml_filename()