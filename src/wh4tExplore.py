#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from sys import stdout

from wh4t.documents import collection
from wh4t.settings import getMailBodyRawFile, getMailBodySymbolsFile, \
                          getMailBodyTokensFile, getMailBodyTypesFile, \
                          getMailBodyWordsFile, getMailBodyStemsFile, \
                          printOwnInfo, printLine, printOK
from wh4t.symbols import symbols

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
       
    printOwnInfo(__file__)
    
    no_of_docs = 0
    
    # Print total file size (=folder size) information of the 
    # input material
    xmlCollection = collection()
    no_of_docs = len(xmlCollection.getDocs())
    print "-- Calculating total file size ..."
    print "Total file size: " + str(xmlCollection.getDocsFileSize()) + \
        " bytes"
    printLine()
    
    # Print total raw text material information, being body text
    # of messages w/o meta-data
    raw_size = xmlCollection.getDocsRawSize()
    print "-- Calculating raw size of text ..."
    print "Total raw size: " + str(raw_size) + " bytes"
    print "Avg raw size: " + str((raw_size / no_of_docs)) + " bytes"
    
    # Write all (body) text to a text file
    stdout.write("Write raw text into file: " + getMailBodyRawFile())
    xmlCollection.writeDocsRawFile()
    printOK()
    
    # - Write all unique symbols like "a", "ö" or "\", which are used, 
    #   into a file
    # - Give number of unique symbols employed
    
    stdout.write("Write symbols used into file: " + getMailBodySymbolsFile())
    syms = symbols()
    syms.writeSymbolsFile()
    printOK() 
    printLine()
    
    print "-- Get unique symbols ..."
    print "Total number of unique symbols: " + str(syms.getNumberOfSymbols())
    printLine()
    
    # Print total numbers of tokens available; separation is done 
    # by means of the Natural Language Toolkit (NLTK)
    # Problematic here: There are lots of non-linguistic tokens being
    # created, like URLs, at this stage.
    # That's why these tokens here are denoted as being "raw".
    print "-- Get tokens ..."
    tokenized_text = xmlCollection.getDocsTokens()
    print "Total number of (raw) tokens: " + \
    str(len(tokenized_text))
    print "Avg number of (raw) tokens: " + \
    str(len(tokenized_text)/no_of_docs)
    printLine()
    
    # - Print total number of unique tokens (=types); also here, lots 
    #   of "non-linguistic" types are preserved, ATM.
    # - Print also these raw types in lower case.
    print "-- Get types ..."
    typed_text = xmlCollection.getDocsTypes()
    typed_text_lowered = xmlCollection.getDocsTypes(lower=True)
    print "Total number of (raw) types: " + \
    str(len(typed_text))
    print "Total number of (raw) types (lower-cased): " + \
    str(len(typed_text_lowered))
    print "Avg number of (raw) types: " + \
    str(len(typed_text)/no_of_docs)
    print "Avg number of (raw) types (lower-cased): " + \
    str(len(typed_text_lowered)/no_of_docs)
    printLine()
    
    # - Print total number of words. These are "real" words; they
    #   are very likely to be of linguistic nature, because they 
    #   were cleaned by the means of regexps -- constructed upon 
    #   observations made.
    print "-- Get number of words ..."
    words = xmlCollection.getDocsWords()
    print "Total number of words: " + \
    str(len(words))
    print "Avg number of words: " + \
    str(len(words)/no_of_docs)
    printLine()
    
    # - Get the subset of nouns from the words
    print "-- Get number of nouns ..."
    nouns = xmlCollection.getDocsWords(pos='n')
    print "Total number of nouns: " + \
    str(len(nouns))
    print "Avg number of nouns: " + \
    str(len(nouns)/no_of_docs)
    print "Total number of (unique) nouns: " + \
    str(len(set(nouns)))
    print "Avg number of (unique) nouns: " + \
    str(len(set(nouns))/no_of_docs)
    printLine()
    
    # - Print total number of unique stems, which got created by NLTK
    #   means, applied over words.
    print "-- Get number of stems ..."
    stemmed_text = xmlCollection.getDocsStems()
    print "Total number of stems: " + \
    str(len(stemmed_text))
    print "Avg number of stems: " + \
    str(len(stemmed_text)/no_of_docs)
    printLine()
    print "-- Get number of unique stems ..."
    stemmed_uniq_text = xmlCollection.getDocsStems(uniq=True)
    print "Total number of unique stems: " + \
    str(len(stemmed_uniq_text)) 
    print "Avg number of stems: " + \
    str(len(stemmed_text)/no_of_docs)
    print "Avg number of (unique) stems: " + \
    str(len(stemmed_uniq_text)/no_of_docs)
    printLine()
    
    # Finally write some files, containing tokens, types, types in
    # lower case, words, stems and nouns.
    
    stdout.write("Write tokens into file: " + getMailBodyTokensFile())
    xmlCollection.writeDocsTokenFile() 
    printOK()
    
    stdout.write("Write types into file: " + getMailBodyTypesFile())
    xmlCollection.writeDocsTypesFile()
    printOK()
    
    stdout.write("Write types (lowered) into file: " + 
                 getMailBodyTypesFile(lower=True))
    xmlCollection.writeDocsTypesFile(lower=True)
    printOK()
    
    stdout.write("Write words into file: " + getMailBodyWordsFile())
    xmlCollection.writeDocsWordsFile()
    printOK()
    
    stdout.write("Write stems (unique) into file: " + getMailBodyStemsFile())
    xmlCollection.writeStemsFile()
    printOK()
    
    stdout.write("Write nouns into file: " + getMailBodyWordsFile(pos='n'))
    xmlCollection.writeDocsWordsFile(pos='n')
    printOK()
    printLine()
    
    # Print the 42 most frequent words -- Zipf's law turns true ;-)
    print "Top 42 words: "
    for stem in xmlCollection.docsTextFreqDist().keys()[:42]: 
        print stem
    printLine()

if __name__ == "__main__":
    main()