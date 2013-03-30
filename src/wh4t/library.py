# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012-2013
(if not noted someone else)
"""
from codecs import open
from os.path import exists
from multiprocessing import cpu_count, Process, Queue
from re import sub, match
import operator
from sys import stdout

from nltk.text import TextCollection
from progressbar import ProgressBar
from xml.etree import cElementTree as ET

from settings import *

class DictFromFile(dict):
    """
    This class represents a file as a dict, reading in all values 
    pairwise, on each line.
    """
    def __init__(self, filename):
        dict.__init__(self)
        f = open(filename, "r", get_def_enc())
        for line in f.readlines():
            pair = line.split()
            self[pair[0]] = float(pair[1])
        f.close()
        
class HashFile(file):
    """
    This class is a file class, specifically representing an 
    hashsums file.
    It's used to encapsulate specifics about its name and existence.
    """
    def __init__(self, mode="r"):
        hash_file = get_hash_file()
        
        if not exists(hash_file):
            print "Hash file doesn't exist."
            print "Create: " + hash_file
            try:
                open(hash_file, "w", get_def_enc()).close()
            except Exception, e:
                print str(e)
        
        file.__init__(self, hash_file, mode)
   
class HashDict(dict):
    """
    This class is a dict class, used to handle the hash file above.
    Each entry in the hash file can be accessed through an object of
    this type.
    """
    def __init__(self):
        dict.__init__(self)
        f = HashFile()
        for line in f.readlines():
            pair = line.split()
            self[pair[0]] = pair[1]
        f.close()
    
    def save(self):
        """
        This method saves the contents of this class to disk.
        """
        f = HashFile(mode="w")
        for pair in self.items():
            f.write(' '.join(map(str, pair)) + '\n')
        f.close()
        
class EnToDeDict(dict):
    """
    This dict provides a primitive dictionary from English to
    German words, w/o ambiguities (in turn w/o any special
    differentiation) used to increase semantic relatedness between
    the different documents we have.
    """
    def __init__(self):
        dict.__init__(self)
        de_en_bidix_file = get_de_en_bidix_file()
        xml_file_handler = ET.parse(de_en_bidix_file)
        p_elems = xml_file_handler.findall(".//p")
        # Only get (both-sided) single word 1:1 mappings
        p_elems_filtered = [p_elem for p_elem in p_elems
                            if len(p_elem.find("l").getchildren()) == 1
                            and len(p_elem.find("r").getchildren()) == 1]
        for p_elem in p_elems_filtered:
            # key: english word; val: german word
            # in lower-case & normalized writing
            self[p_elem.find("r").text.lower()] = \
                normalize_word(p_elem.find("l").text.lower())
                
class Synsets(list):
    """
    This list holds synsets, i. e. words semantically grouped with
    each other.
    """
    def __init__(self):
        list.__init__(self)
        synsets_file = get_synsets_file()
        f = open(synsets_file, "r", get_def_enc())
        lines = f.readlines()
        f.close()
        
        for line in lines:
            if line[0] == "#":
                continue
            synset = self._clean_synset(line.split(";"))
            if len(synset) >= 2:
                self.append(synset)
            
    def _clean_synset(self, synset):
        """
        Internal method which removes certain expressions from
        a synset.
        @param: Synset (as list)
        @return: A clean synset (as list)
        """
        clean_synset = list()
        lang_levels = ["umgangssprachlich", "derb", "vulgär", 
                       "fachsprachlich", "gehoben"]
        for word in synset:
            for lang_level in lang_levels:
                word = sub(" \("+lang_level+"\)", "", word)
            if match(".*[ \(\)].*", word) == None:
                clean_synset.append(normalize_word(word.lower()))
                
        return clean_synset
           
def normalize_word(word_to_normalize):
    """
    This function helps to normalize words in order to make
    them better comparable.
    @return: Normalized word as str type
    """
    
    # Transform umlauts to ASCII
    word = word_to_normalize.replace(u"Ä","Ae").replace(u"Ö","Oe"). \
        replace(u"Ü","Ue").replace(u"ä","ae").replace(u"ö","oe"). \
        replace(u"ü","ue").replace(u"ß","ss")
    # Remove stuff around words, like citation symbols, interpunctation
    # and return word
    return sub("\W+$", "", sub("^\W+", "", word))

def split_term(term):
    """
    This function splits a term into several words, e. g.
    "Diktatur-Kontrolle" will become ["Diktatur", "Kontrolle"]
    @param term:  A term to split being a string
    @return List with splitted words
    """
    return sub("[,-.&|]+", "#", term).split("#") # Split also "Dr.-Ing"
        
def rreplace(s, old, new, occurrence):
    """
    
    Replaces a string from right to left (reverse) by allowing for
    specification of how many occurrences should be replaced.
    @param s: String to be altered.
    @param old: Substring to replace.
    @param new: New substring to put in place.
    @param occurrence: Number of substitutions (from right to left) to
                       carry out.
    @return: New string, after desired substitutions.
    
    From public domain source by "mg.", 2010: 
    * http://stackoverflow.com/questions/2556108/
      rreplace-how-to-replace-the-last-occurence-of-an
      -expression-in-a-string
    
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)

def clean_iterable(iter_to_clean):
    """
    @param iter_to_clean: An iterable whose elements should be freed from 
                    whitespaces.
    @return: Return iterable freed from whitespaces.
    """
    return map(lambda s : s.strip(), iter_to_clean)

def get_nltk_text_collection(xmlcollection):
    """
    @param xmlcollection: A collection of all (as of now) XML 
                          documents, of type collection.
    @return: Retrieves an NLTK TextCollection with all stems from our 
             document collection.
    """
    nltk_textcollectionList = list()
    
    print "Creating NLTK text collection ... "
    xmlcollection_list = xmlcollection.get_docs()
    
    pb = ProgressBar(maxval=len(xmlcollection_list)).start()
    cnt = 0
    for doc in xmlcollection_list:
        cnt += 1
        pb.update(cnt)
        nltk_textcollectionList.append(list(doc.get_stems()))
        
    return TextCollection(nltk_textcollectionList)

def get_classification_stems(stems, idf_dict):
    """
    This function removes most frequent and all very rare stems (single
    occurrence), to improve classification results.
    @param stems: List of stems to be filtered
    @param idf_dict: Dictionary containing the idf values to filter
                     after
    @return: List with out-filtered stems
    """ 
    max_val = max(idf_dict.itervalues()).as_integer_ratio()
    return [stem for stem in stems
            if idf_dict[stem] > get_def_idf_filter_val()
            and not idf_dict[stem].as_integer_ratio() == max_val]
    
def get_top_ranked_idf_terms(terms):
    """
    This functions returns the top (10) ranked idf terms passed.
    @param terms: An iterable with terms to be sorted after values, in
                  this case idf values; biggest first.
    @return: List with top ranked idf terms.
    """
    max_len = 10
    
    idf_file = get_stems_file(measure="_idf")
    idf_dict = DictFromFile(idf_file)
    
    terms_dict = dict()
    for term in terms:
        terms_dict[term] = idf_dict[term]
    
    terms_sorted = [term[0] for term in sorted(terms_dict.items(), 
                    key=lambda x: x[1], reverse=True)]
    
    if len(terms_sorted) > max_len:
        return terms_sorted[:max_len]
    
    return terms_sorted

def write_tfidf_file(xmlcollection, nltk_textcollection):
    """
    Writes a tf*idf matrix file with all tf*idf values for each 
    document, row by row. The columns represent the (alphabetically
    ordered) stems available in the whole collection.
    @param xmlcollection: Collection of XML documents, type collection
    @param nltk_textcollection: NLTK TextCollection of all the stems
    """
    idf_file = get_stems_file(measure="_idf")
    avg_words_per_doc = len(xmlcollection.get_words()) / \
                        len(xmlcollection.get_docs())

    if not exists(idf_file):
        write_idf_file(xmlcollection, nltk_textcollection)

    idf_dict = DictFromFile(idf_file)
    tfidf_dict = dict()
    high_tfidf_stems = set()
    
    collection_stems = list(xmlcollection.get_stems(uniq=True))
    print "Length of collection, all stems:", len(collection_stems)
    
    # Remove most frequent (idf<2) / stop stems (or qualifying 
    # as such), and most rare stems (max(idf)), as they are of no 
    # help to separate / make up clusters
    collection_stems = get_classification_stems(collection_stems, idf_dict)
    print "Length of collection, cluster stems:", len(collection_stems)
    
    f = open(get_tfidf_matrix_file(), "w", get_def_enc())
    for doc in xmlcollection.get_docs():
        doc_stems = doc.get_stems()
        col = TextCollection("")
        
        stdout.write(doc.get_id())
        idf_row = ""
        stdout.write(" (")
        for stem in sorted(collection_stems):
            tf = col.tf(stem, doc_stems)
    
            # Reweight tf values, to get more classifcation words
            # and compensate for the very different document sizes 
            # available
            # Idea: Accounts for average document length, but also for
            # the number of times a word effectively occurs in a 
            # specific document; other variations can be thought of 
            # (using log) or maximal tf values
            # Note: The clustering works better with (in general)
            # smaller values
            if tf > 0.0:
                tf = 1.0 / avg_words_per_doc * tf
            # If nothing applies: tf is 0.0
                
            tfidf = tf*float(idf_dict[stem])
            tfidf_dict[stem] = tfidf

            # We may find here some threshold that makes sense
            if (tfidf > 0.0):
                stdout.write(stem + ", ")
                high_tfidf_stems.add(stem)
            
            idf_row += str(tfidf) + " "
        f.write(idf_row + "\n")
        stdout.write(")\n")
    f.close()
    print "List length of high value tf*idf terms:", len(high_tfidf_stems)
    
    sorted_tfidf_dict = \
        sorted(tfidf_dict.iteritems(), reverse=True,
               key=operator.itemgetter(1))
    
    f = open(get_stems_file(measure="_tfidf_sorted"), "w", get_def_enc())
    for pair in sorted_tfidf_dict: 
        f.write(str(pair[1]) + " " + pair[0] + "\n")
    f.close()
    
  
def write_idf_file(xmlcollection, nltk_textcollection):
    """
    Writes a (collection-wide) file with idf valus for each stem.
    @param xmlcollection: Collection of XML documents, type collection
    @param nltk_textcollection: NLTK TextCollection of all the stems
    """
    print "Calculating idf values for all stems ..."
    all_stems = xmlcollection.get_stems(uniq=True)
    idfset = set()
    pb = ProgressBar(maxval=len(all_stems)).start()
    cnt = 0
    for word in all_stems:
        cnt += 1
        pb.update(cnt)
        idf = nltk_textcollection.idf(word)
        if idf > 0.0: 
            idfset.add((idf, word))
    
    f = open(get_stems_file(measure="_idf"), "w", get_def_enc())
    for pair in sorted(idfset, reverse=True): 
        f.write(pair[1] + " " + str(pair[0]) + "\n")
    f.close()
    
def exists_tfidf_matrix(xmlcollection, create=False):
    """
    This method checks for the existence of a TF*IDF matrix, and may
    invoke its creation.
    
    @param create: Boolean optional value indicating if TF*IDF 
                   matrix should be created if not already existent.
                   Defaults to "no".
    @param xmlcollection: It's possible to pass an object reference
                          with the XML collection a TF*IDF matrix
                          should be created for. Defaults to the full
                          collection if nothing given AND a TF*IDF
                          matrix is not present already.
    @return: Boolean value being True or False, indicating if a TF*IDF 
             matrix could be found or created.
             
    """
    retval = False
    
    if not exists(get_tfidf_matrix_file()):
        print "TF*IDF matrix seems not available."
        if create is True:
            nltk_textcollection = get_nltk_text_collection(xmlcollection)
            write_tfidf_file(xmlcollection, nltk_textcollection)
            print "TF*IDF matrix written to: ", get_tfidf_matrix_file()
            retval = True
    else:
        print "TF*IDF matrix seems available: ", get_tfidf_matrix_file()
        retval = True
        
    return retval

def get_positional_index(tfidf_matrix_file):
    """
    Upon a TF*IDF matrix (with lots of zero positions) a positional
    index is created, indicating which documents contain which terms
    (by their position)
    
    @param tfidf_matrix_file: File path to the (already created) TF*IDF
                              matrix.
    @return: Nested lists representing for each document which terms
             (by position) they contain.
    """
    pos_idx = list()
    
    f = open(tfidf_matrix_file, "r", get_def_enc())  
    doc_count = 0
    while True:
        doc_line = f.readline()
        # Leave loop when last document line is reached
        if doc_line == "":
            break
        doc_count += 1
        termscore_list = doc_line.split(" ")
        termscore_list.pop() # Hack for now, because last elem is void
        
        idx = list() # To hold non-zero TF*IDF positions
        termscore_count = 0
        for termscore in termscore_list:
            termscore_count += 1
            if float(termscore) > 0.0:
                idx.append(termscore_count)
            
        pos_idx.append(idx)
    
    f.close()
    
    return pos_idx

def filter_subsets(iter_, nested=False):
    """
    
    Removes all (proper and not proper) subsets from an iterable,
    that has a list of lists structure.
    
    @param iter: An iterable, e. g. a list, to be cleaned.
    @param nested: If True we handle nested structures. Only the first
                   list in a list is filtered, then the nested 
                   structure is reconstructed.
    @return: Filtered list
    
    List comprehension from public domain source by "Triptych", 2009:
    http://stackoverflow.com/questions/1318935/
    python-list-filtering-remove-subsets-from-list-of-lists
    @author: Triptych. http://stackoverflow.com/users/43089/triptych
    
    """
    iter_orig = list()
    
    # If nested list of lists given, 
    # prepare for filtering only first elements
    if nested == True:
        iter_orig = iter_
        iter_ = list()
        for elem in iter_orig:
            iter_.append(elem[0])
    
    # Filter out all subsets
    iter_ = [x for x in iter_ 
            if not any(set(x) <= set(y) for y in iter_ if x is not y)]
    
    # Reconstruct neglected nested parts, after filtering
    if nested == True:
        iter_reconstructed = list()
        for elem in iter_orig:
            if elem[0] in iter_:
                iter_reconstructed.append(elem)
        return iter_reconstructed
    
    return iter_

def spawn_processes(f, iter_):
    """
    
    This function creates various processes for
    a function f which has an argument iter_
    (an iterable) to process.
    
    It does it by creating smaller iterables and processing
    them independently, then uniting the results.
    
    @f: A function f
    @iter_: The argument of function f, being an iterable
    """
    cpu_count_ = cpu_count()
    iter_size = len(iter_)
    ret_iter = list()
    max_processes = 1
    
    print "Orig iterable size:", iter_size
    
    if cpu_count > 2:
        max_processes = cpu_count_ - 1
        
    if max_processes > 1:
        iter_sizes = list()
        processes_list = list()
        queues_list = list()
        base_iter_len = iter_size / max_processes
        residual_val = iter_size % max_processes
        
        # Create iterable sizes
        iter_count = 0
        while True:
            if (iter_count == max_processes):
                break
            iter_sizes.append(base_iter_len)
            iter_count += 1
        if residual_val > 0:
            iter_sizes[0] += residual_val
        print "Iterable sizes:", iter_sizes
        
        # Split iterables
        iters_list = list()
        start_pos = 0
        end_pos = iter_sizes[0]
        for idx_start in range(len(iter_sizes)):
            idx_end = idx_start + 1
            print start_pos, end_pos
            iters_list.append(iter_[start_pos:end_pos])
            start_pos += iter_sizes[idx_start]          

            if (idx_end == len(iter_sizes)):
                break
            
            end_pos += iter_sizes[idx_end]

        # Launch processes
        for i in range(len(iters_list)):
            queues_list.append(Queue())
            processes_list.append(Process(target=f, 
                            args=(iters_list[i], queues_list[i])))
            processes_list[i].start()
        
        # Wait for all processes to finish
        for i in range(len(processes_list)):
            processes_list[i].join()
            
        # Unite solution space
        for i in range(len(queues_list)):
            for elem in queues_list[i].get():
                ret_iter.append(elem)
        
        return sorted(ret_iter)
        
    return f(iter_)

class ListByLen(list):
    """
    @author Arian Sansui <arian@sanusi.de, 2012
    @author Hernani Marques <h2m@access.uzh.ch>, 2012 (some adaptions)
        
    It's used like the following:
    from list_by_len import ListByLen
    regularlist = list(["a","wuff","miau","yeah","koffer",
                        "hamsterföderation","hamsterföderative"])
    print regularlist
    ['a', 'wuff', 'miau', 'yeah', 'koffer', 'hamsterf\xc3\xb6deration',
     'hamsterf\xc3\xb6derative']

    newlist = ListByLen(regularlist)[1:4]
    print newlist
    ['a', 'wuff', 'miau', 'yeah']
    """    
    def __getitem__(self, length):
        """
        @return: [ i for i in self if len(i) == length]
        """ 
        return ListByLen( ( i for i in self if len(i) == length ) )
        
    def __getslice__(self, start, end):
        """
        @param start: Start of subset of list we want.
        @param end: End of subset of list we want.
        @return: List (subset) from a given start to the end.
        """   
        a = ListByLen()
        for length in range(start, end + 1):
            a.extend(self[length])
        return a

#################
# General getters
#################

def get_own_info(calling_file):
    """
    @return: A string indicating this software package, the filename --
             specific to the calling file object -- and the version 
             number.
    """
    prog_name = sub(".py", "", basename(calling_file))
    prog_name = sub("_", "", prog_name, 1)
    info_string = "wahatttt" + " v" + VERSION+" - " + sub("wh4t", 
                                                          "", 
                                                          prog_name)
    return info_string

def get_def_no_of_topwords():
    """
    @return: The number of top words set by default used when at some
             point top words by frequency are displayed / written.
    """
    return DEFAULT_NUMBER_OF_TOPWORDS

def get_def_editdistance_filename_suffix():
    """
    @return: Defined suffix when not specified 
    """
    return DEFAULT_EDITDISTANCE_FILENAME_SUFFIX

def get_def_len_for_editdistancing():
    """
    @return: Default int number for queries being made by edit distance.
    """
    return DEFAULT_LEN_FOR_EDITDISTANCING

def get_def_no_of_clusters():
    """
    @return: Returns number of clusters to create
    """
    return DEFAULT_NUMBER_OF_CLUSTERS

#######################################################################
# Getters for file names, needed in other classes, to read or write 
# files.
# See definitions section for more information on its intended content.
#######################################################################

def get_web_output_dir():
    """
    @return: String with path to a folder where web output vor data
             visualization lies
    """
    return WEB_OUTPUT_DIR

def get_mailfolder(content_format="XML"): 
    """
    @param: If type's "CSV" return mail folder where mails in CSV 
            format lie
    @return: String with mail folder path of the input data
    """
    if content_format == "line":
        return MAIL_FOLDER_LINE
    
    # Fallback case "XML"
    return MAIL_FOLDER_XML

def get_clustdir():
    """
    @return: Return a path as string with the clusters' dir
    """
    return PROJ_CLUST_DIR + t.datetime.now().strftime("%Y%m%d_%Hh%Mm") + sep

def get_wordsdir(pos='_'):
    """
    @param: If pos is 'n' return a path to store nouns, otherwise to 
            store words in general.
    @return: Return a path as string to store words by document
    """
    if (pos == 'n'): 
        return PROJ_NOUNS_DIR
    # Default
    return PROJ_WORDS_DIR

def get_stemsdir():
    """
    Return stems directory path
    
    @return: String with dir path
    
    """
    return PROJ_STEMS_DIR

def get_invalid_xml_filename(): 
    """
    @return: String to a file path for invalid XML documents
    """
    return INVALID_XML_FILENAME

def get_def_enc(): 
    """
    @return: String of the default encoding engaged
    """
    return DEFAULT_ENCODING

def get_raw_file(): 
    """
    @return: String with path to a file for all the raw content
    """
    return RAW_FILE

def get_symbols_file(): 
    """
    @return: String to a file for storing all the symbols used
    """
    return SYMBOLS_FILE

def get_proj_basedir(): 
    """
    @return: String with path for the project's main/root directory
    """
    return PROJ_BASE_DIR

def get_tokens_file(): 
    """
    @return: String with file path for holding the tokens in use
    """
    return TOKENS_FILE

def get_types_file(lower=False):
    """
    @param lower: Indicate if tokens file shall contain only 
                  lower case letters (=True), otherwise file shall
                  be in mixed cases
    @return: String with file path to the file feat. types (=unique
             tokens), either mixed or only lower cased
    """ 
    if lower == False:
        return TYPES_FILE
    return TYPES_LOWERED_FILE

def get_words_file(pos='_'): 
    """
    @param pos: When '_' all words, when 'n' nouns file
    @return: String with file path where found words are written to 
    """
    if (pos == 'n'):
        return NOUNS_FILE
    
    return WORDS_FILE

def get_words_corr_file():
    """
    @return: Returns file path to a file which lists corrected words.
    """
    return WORDS_CORRECTED_FILE

def get_stems_file(measure=""): 
    """
    @pos measure: If a special measure is saved in this file. 
                  Something that makes sense to be stored along 
                  with the nouns is their "IDF" values.
    @return: String with file path to hold the unique stems encountered
             (along with other info)
    """
    return STEMS_FILE + measure

def get_words_by_editdistance_file(
    editdistance=get_def_editdistance_filename_suffix()):
    """
    @param: Positive integer specifying of which edit distance the word
            pairs are
    @return: String with file path to store pairs of words 
             edit-distanced by a specified length
    """
    filename = WORDS_BY_EDITDISTANCE_FILE
    return filename + str(editdistance)

def get_topwords_file(): 
    """
    @return: String with file path to store the most frequent words
    """
    return TOPWORDS_FILE

def get_nouns_file(measure=""):
    """
    @return: String with file path to store nouns
    """
    return NOUNS_FILE + measure

def get_hash_file():
    """
    @return: String with file path to store hash sums of files
    """
    return HASH_FILE

def get_tfidf_matrix_file():
    """
    @return: String with file path to tf*idf values of all stems for
             all documents
    """
    return TFIDF_MATRIX

def get_de_en_bidix_file():
    """
    @return: String with file path to de-en bidictionary file.
    """
    return DE_EN_BIDIX_FILE

def get_synsets_file():
    """
    @return: String with file path to synsets file.
    """
    return SYNSETS_FILE

def get_def_idf_filter_val():
    """
    @return: A float indicating a maximum IDF value tolerated
    """
    return DEFAULT_IDF_FILTER_VALUE

def get_def_common_terms_no():
    """
    @return: Return number (int) of occurrences necessary to cluster
             documents.
    """
    return DEFAULT_COMMON_TERMS_NUMBER

def get_def_graph_name():
    """
    @return: Return default graph name for web visualization
    """
    return DEFAULT_GRAPH_NAME

def get_graph_file(filename=get_def_graph_name()):
    """
    @return: String with path to graph file
    """
    return get_proj_basedir() + filename + ".yaml"

def get_webgraph_res():
    """
    @return: 2-element tuple with width and height
             representing the webgraph's resolution
    """
    return DEFAULT_WEBGRAPH_RESOLUTION

###################################
# Simple printer / helper functions
###################################

def print_line(): 
    """
    To create semi-graphical lines used to seperate output on the 
    terminal
    """
    print 78*"*"

def print_ok(): 
    """
    To indicate on the terminal something went OK, e. g. creation of a
    file
    """
    print(" -- OK")
    
def print_own_info(calling_file):
    """
    Prints information about the file that includes and uses this
    function to the terminal.
    @param: Object of the file we want information about, usually the
            calling file.
    """
    print_line() 
    print get_own_info(calling_file)
    print_line()