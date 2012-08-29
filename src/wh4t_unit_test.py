#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from sys import stdout

from codecs import open
import enchant
from nltk.metrics import edit_distance
from progressbar import ProgressBar
from re import match

from wh4t.documents import Collection
from wh4t.settings import print_line, print_own_info, get_words_corr_file, \
     get_def_enc
from wh4t.nouns import Nouns
from wh4t.library import EnToDeDict, Synsets

def main():
    """ 
    Unit tests for different components of the system.
    
    """
    print_own_info(__file__)
    spellcheck_test()
    """
    print_line()
    en_to_de_dict_test()
    print_line()
    synsets_test()
    print_line()
    single_document_stats(42)
    print_line()
    """
    
def spellcheck_test():
    d = enchant.Dict("de_DE")
    words = set(Collection().get_words())
    no_words = len(words)
    no_corrected_words = 0
    no_words_ok = 0
    pb = ProgressBar(maxval=no_words).start()
    word_no = 1
    
    f = open(get_words_corr_file(), "w", get_def_enc())
    for word in words:
        pb.update(word_no)
        stdout.write("Words OK (curr word no) / no of total words" +
                     " [actual correction]: ")
        stdout.write(str(no_words_ok) + " ("+ str(word_no) +") / " 
                     + str(no_words))
        word_corrected = None
        if d.check(word) == False:
            sugg_list = d.suggest(word)
            if len(sugg_list) > 0:
                word_corrected = sugg_list[0]
                # (1) Make sure the spell checking's doesn't go too 
                #     wild / experimental by enforcing a (maximum)
                #     edit distance tolerated
                # (2) Make sure the change happens not in the first
                #     position; i. e. "haus" -> "Haus" is not what's
                #     interesting
                # (3) Also make sure that potential abbreviations like
                #     "CCC" or "MR" don't get changed
                if edit_distance(word, word_corrected) == 1 and \
                   word[0] == word_corrected[0] and \
                   match("[A-Z]{2,}", word) == None:
                    no_corrected_words += 1
                    print " [" + str(no_corrected_words) + ":", \
                          word, " -> ", word_corrected + "]"
                    f.write(word + "\t" + word_corrected + "\n")
                    f.flush() # For the sake of tail(1)
                else:
                    print ""
            else:
                print ""
        else:
            print ""
            no_words_ok += 1
        word_no += 1
    f.close()
                             
    print no_corrected_words, "/", no_words
    
def en_to_de_dict_test():    
    d = EnToDeDict()
    for eng_w, deu_w in d.items():
        print eng_w, " -> ", deu_w
    print len(d)

def synsets_test():
    s = Synsets()

    for synset in s:
        print str(synset)
    
    print len(s)

def single_document_stats(doc_no):
    xmldocuments = Collection()
    # Get a specific doc number for tests
    xmldocument = xmldocuments.get_doc(doc_no)
    
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

if __name__ == "__main__":
    main()