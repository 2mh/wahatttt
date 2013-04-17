#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from sys import stdout

from wh4t.documents import Collection
from wh4t.library import get_raw_file, get_symbols_file, get_tokens_file, \
                         get_types_file, get_words_file, get_stems_file, \
                         print_own_info, print_line, print_ok
from wh4t.symbols import Symbols

#####################
# Program starts here
#####################

def main():
    """
    This program makes a first exploration of all the input
    material we have, it prints out information like:
    - How big the input folder is (bytes)
    - How many raw text material is available (bytes), i. e. 
      w/o meta-data
    - How many symbols are used 
    - How many tokens, words, stems etc. are available
    
    TBD: 
    - Add params to this program or make it more user-friendly /
      interactive.
    - Add more outcome, probably not only quantitative, but also
      qualitative information.
    - Put some of the (verbose) text into other classes.
    """
       
    print_own_info(__file__)
    
    # Print total file size (=folder size) information of the 
    # input material
    xmldocs = Collection()
    no_of_docs = len(xmldocs.get_docs())
    print "-- Calculating total file size ..."
    print "Total file size: " + str(xmldocs.get_filesize()) + " bytes"
    print_line()
    
    # Print total raw text material information, being body text
    # of messages w/o meta-data
    rawsize = xmldocs.get_rawsize()
    print "-- Calculating raw size of text ..."
    print "Total raw size: " + str(rawsize) + " bytes"
    print "Avg raw size: " + str((rawsize / no_of_docs)) + " bytes"
    
    # Write all (body) text to a text file
    stdout.write("Write raw text into file: " + get_raw_file())
    xmldocs.write_raw_text(in_one_file=True)
    print_ok()
    
    # - Write all unique symbols like "a", "ö" or "\", which are used, 
    #   into a file
    # - Give number of unique symbols employed
    
    stdout.write("Write symbols used into file: " + get_symbols_file())
    syms = Symbols()
    syms.write_symbols()
    print_ok()
    print_line()
    
    print "-- Get unique symbols ..."
    print "Total number of unique symbols: " + str(syms.get_no_of_symbols())
    print_line()
    
    # Print total numbers of tokens available; separation is done 
    # by means of the Natural Language Toolkit (NLTK)
    # Problematic here: There are lots of non-linguistic tokens being
    # created, like URLs, at this stage.
    # That's why these tokens here are denoted as being "raw".
    print "-- Get tokens ..."
    tokenized_text = map(lambda x:x.lower(), xmldocs.get_tokens())
    print "Total number of (raw) tokens: " + str(len(tokenized_text))
    print "Avg number of (raw) tokens: " + \
        str(len(tokenized_text)/no_of_docs)
    print_line()
    
    # - Print total number of unique tokens (=types); also here, lots 
    #   of "non-linguistic" types are preserved, ATM.
    # - Print also these raw types in lower case.
    print "-- Get types ..."
    typed_text = xmldocs.get_types()
    typed_text_lowered = xmldocs.get_types(lower=True)
    print "Total number of (raw) types: " + \
    str(len(typed_text))
    print "Total number of (raw) types (lower-cased): " + \
    str(len(typed_text_lowered))
    print "Avg number of (raw) types: " + \
    str(len(typed_text)/no_of_docs)
    print "Avg number of (raw) types (lower-cased): " + \
    str(len(typed_text_lowered)/no_of_docs)
    print_line()
    
    # - Print total number of words. These are "real" words; they
    #   are very likely to be of linguistic nature, because they 
    #   were cleaned by the means of regexps -- constructed upon 
    #   observations made.
    print "-- Get number of words ..."
    words = xmldocs.get_words()
    words2 = set(words)
    print "Total number of words: " + \
    str(len(words))
    print "Total number of words2: " + \
    str(len(words2))
    print "Avg number of words: " + \
    str(len(words)/no_of_docs)
    print_line()
    
    # - Get the subset of nouns from the words
    print "-- Get number of nouns ..."
    nouns = xmldocs.get_words(pos='n')
    print "Total number of nouns: " + \
    str(len(nouns))
    print "Avg number of nouns: " + \
    str(len(nouns)/no_of_docs)
    print "Total number of (unique) nouns: " + \
    str(len(set(nouns)))
    print "Avg number of (unique) nouns: " + \
    str(len(set(nouns))/no_of_docs)
    print_line()
    
    # - Print total number of unique stems, which got created by NLTK
    #   means, applied over words.
    print "-- Get number of stems ..."
    stemmed_text = xmldocs.get_stems()
    print "Total number of stems: " + \
    str(len(stemmed_text))
    print "Avg number of stems: " + \
    str(len(stemmed_text)/no_of_docs)
    print_line()
    print "-- Get number of unique stems ..."
    stemmed_uniq_text = xmldocs.get_stems(uniq=True)
    print "Total number of unique stems: " + \
    str(len(stemmed_uniq_text)) 
    print "Avg number of stems: " + \
    str(len(stemmed_text)/no_of_docs)
    print "Avg number of (unique) stems: " + \
    str(len(stemmed_uniq_text)/no_of_docs)
    print_line()
    
    # Finally write some files, containing tokens, types, types in
    # lower case, words, stems and nouns.
    
    stdout.write("Write tokens into file: " + get_tokens_file())
    xmldocs.write_tokens() 
    print_ok()
    
    stdout.write("Write types into file: " + get_types_file())
    xmldocs.write_types()
    print_ok()
    
    stdout.write("Write types (lowered) into file: " + 
                 get_types_file(lower=True))
    xmldocs.write_types(lower=True)
    print_ok()
    
    stdout.write("Write words into file: " + get_words_file())
    xmldocs.write_words()
    print_ok()
    
    stdout.write("Write stems (unique) into file: " + get_stems_file())
    xmldocs.write_stems()
    print_ok()
    
    stdout.write("Write nouns into file: " + get_words_file(pos='n'))
    xmldocs.write_words(pos='n')
    print_ok()
    print_line()
    
    # Print the 42 most frequent words -- Zipf's law turns true ;-)
    print "Top 42 words (most frequent): "
    for stem in xmldocs.get_freqdist().keys()[:42]: 
        print stem
    print_line()
    
    # Print the 42 most relevant words -- after tf*idf measure
    print "Top 42 words (most relevant): "
    # ...

if __name__ == "__main__":
    main()