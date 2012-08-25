#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from wh4t.documents import Collection
from wh4t.settings import print_line
from wh4t.nouns import Nouns
from wh4t.library import EnToDeDict, Synsets

"""
d = EnToDeDict()
for eng_w, deu_w in d.items():
    print eng_w, " -> ", deu_w
print len(d)
"""

s = Synsets()

for synset in s:
    print str(synset)

print len(s)

"""
# Program starts here
xmldocuments = Collection()
# Get a specific doc number for tests
xmldocument = xmldocuments.get_doc(51)

# Print raw content, tokens and then types (mixed- and lowercase)
print_line()
print "Print raw content: "
print xmldocument.get_rawcontent()
print_line()
print "Print tokens: "
print xmldocument.get_tokens()
print_line()
print "Print types (mixed-case): "
print xmldocument.get_types()
print_line()
print "Print types (lower-case): "
print xmldocument.get_types(lower=True)
print_line()
print "Print words: "
print xmldocument.get_words()
print_line()
print "Print nouns: "
print xmldocument.get_words(pos='n', ref_nouns=Nouns())
print_line()
print "Print stems: "
print xmldocument.get_stems()
print_line()
"""
