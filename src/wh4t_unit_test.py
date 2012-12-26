#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from sys import stdout

from codecs import open
import enchant
from nltk.metrics import edit_distance
from progressbar import ProgressBar
from collections import defaultdict

from wh4t.documents import Collection
from wh4t.settings import print_line, print_own_info, get_words_corr_file, \
     get_def_enc
from wh4t.nouns import Nouns
from wh4t.library import spawn_processes, EnToDeDict, Synsets

def main():
    """ 
    Unit tests for different components of the system.
    
    """
    print_own_info(__file__)
    # print spawn_processes(test_function, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # spawn_processes(translate_words, Collection().get_words())
    """
    print_line()
    en_to_de_dict_test()
    single_document_stats(42)
    print_line()
    """
    synsets_test()
    print_line()
    
def test_function(iter_, queue):
    """
    
    @param iter_: 
    @param queue: A Queue() object (from package multiprocessor)
                  used here to put in the partial solution,
                  needed for multiprocessing
    
    """
    
    ret_iter = list()
    
    for i in iter_:
        val = i * i
        ret_iter.append(val)
    
    queue.put(ret_iter)
    return ret_iter
    
def translate_words(words, queue):
    d_en_de = EnToDeDict()
    words = set(words)
    no_words = len(words)
    word_no = 1
    words_translated = 0
    
    # First replace English words by German ones
    words_tmp = sorted(words.copy())
    print "Start word-to-word translation (EN -> DE) ..."
    pb = ProgressBar(maxval=no_words).start()
    for word in words_tmp:
        pb.update(word_no)
        if word in sorted(d_en_de.keys()):
            words.remove(word)
            words.add(d_en_de[word])
            print word, "->", d_en_de[word]
            words_translated += 1
        word_no += 1
    print "Translation fulfilled (" + str(words_translated) \
          + " translations)."
          
    queue.put(words)
        
def spellcheck_test():
    d = enchant.Dict("de_DE")
    d_en_de = EnToDeDict()
    words = set(Collection().get_words())
    no_words = len(words)
    word_no = 1
    words_translated = 0
    
    # First replace English words by German ones
    words_tmp = sorted(words.copy())
    print "Start word-to-word translation (EN -> DE) ..."
    pb = ProgressBar(maxval=no_words).start()
    for word in words_tmp:
        pb.update(word_no)
        if word in sorted(d_en_de.keys()):
            words.remove(word)
            words.add(d_en_de[word])
            print word, "->", d_en_de[word]
            words_translated += 1
        word_no += 1
    print "Translation fulfilled (" + str(words_translated) \
          + " translations)."
    
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
                # (3) Also make sure that words with length <= 5 don't
                #     get changed
                if edit_distance(word, word_corrected) == 1 and \
                   word[0] == word_corrected[0] and \
                   len(word) > 5:
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
    synsets = Synsets()
    words_all_uniq = set()
    words_not_ambig = set()
    synsets_freq_dict = defaultdict(int)

    # Print every synset and create set of all words found
    for synset in synsets:
        print str(synset)
        for word in synset:
            words_all_uniq.add(word)
            synsets_freq_dict[word] += 1
            
    for word, count in synsets_freq_dict.items():
        # We are only interestd in words which appear only in one
        # synset.
        if count == 1:
            words_not_ambig.add(word)
            
    # Clean synsets (to only have synsets w/ clear meaning)
    new_synsets = list()
    count = 0
    for synset in synsets:
        count += 1
        for word in words_not_ambig:
            print count, synset
            if word in synset:
                new_synsets.append(synset)
                break
    
    print "Total number of synsets:", len(synsets)
    print "Number of words involved (unique):", len(words_all_uniq)
    print "Number of words (w/ one meaning)", len(words_not_ambig)
    print "Total number of synsets (after cleaning):", len(new_synsets)

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