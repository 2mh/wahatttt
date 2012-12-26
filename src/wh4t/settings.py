# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
import datetime as t
from os import sep
from os.path import basename, abspath, join, pardir, curdir
from re import sub

################
# Default values
################

# Version of the wahatttt system as a whole; as of 1.0 it'll be usable
VERSION = "0.82"

# Ensure everything's using one encoding only (here: UTF-8).
DEFAULT_ENCODING = "UTF-8"

# The number of top words (by frequency) displayed / written when 
# not further specified. This is used in different contexts.
DEFAULT_NUMBER_OF_TOPWORDS = 42

# This int is the default number for how long source words used to 
# check against others -- by the measure of edit distance -- 
# should be. 0 is implemented to mean "of any length".
DEFAULT_LEN_FOR_EDITDISTANCING = 0

# That's the default suffix a filename with word pairs in within 
# some edit distance contains.
DEFAULT_EDITDISTANCE_FILENAME_SUFFIX = ""

# Number of clusters to create (for now used for the neuronal 
# clustering)
DEFAULT_NUMBER_OF_CLUSTERS = 4

# Up to which level the frequent terms should be filtered out
# -- according to their IDF (inverse document frequency) values
# Caution: When changes doesn't recreate a new TF*IDF matrix.
DEFAULT_IDF_FILTER_VALUE = 2.0

# Number of terms which must match in order to cluster two documents.
# With a number of 5 (empirically tested) for ~99% of the documents a
# cluster with at least two documents can be constructed, i. e. if
# DEFAULT_IDF_FILTER_VALUE = 2.0. If higher, then much less is possible,
# as more frequent terms get removed.
DEFAULT_COMMON_TERMS_NUMBER = 300

##########################
# Paths to folders / files
##########################

# The project's base path relative to the position of this 
# settings file.
PROJ_BASE_DIR = abspath(join(curdir, pardir)) + sep

# The project's (freely available linguistic) resources directory
PROJ_RES_DIR = PROJ_BASE_DIR + "resources" + sep

# Directories where clusters, words, nouns, stems are hold, per document and
# file by file
PROJ_CLUST_DIR = PROJ_BASE_DIR + "clust_dir" + sep
PROJ_WORDS_DIR = PROJ_BASE_DIR + "words_dir" + sep
PROJ_NOUNS_DIR = PROJ_BASE_DIR + "nouns_dir" + sep
PROJ_STEMS_DIR = PROJ_BASE_DIR + "stems_dir" + sep

# XML file containing info about broken XML files, if any
# (hopefully not).
INVALID_XML_FILENAME = PROJ_BASE_DIR + "invalid_input_docs.xml"

# Text file with all (body) content available, in raw form.
RAW_FILE = PROJ_BASE_DIR + "raw"

# Text file with list of all symbols used in the mail body
SYMBOLS_FILE = PROJ_BASE_DIR + "symbols"

# File with list of all tokens used, from the raw text
# (in the given order)
TOKENS_FILE = PROJ_BASE_DIR + "tokens"

# File with list of all unique tokens (=types) used
TYPES_FILE = PROJ_BASE_DIR + "types"

# File with list of all unique tokens used in lowered form
TYPES_LOWERED_FILE = PROJ_BASE_DIR + "types_lowercase"

# File with list of all words (=cleaned tokens), in the given order
WORDS_FILE = PROJ_BASE_DIR + "words"

# File with list of all corrected words (after controlled
# spellchecking)
WORDS_CORRECTED_FILE = PROJ_BASE_DIR + "words_corrected"

# File with nouns in the collection, is a subset of nouns.
NOUNS_FILE = PROJ_BASE_DIR + "nouns"

# File with pairs of words by a specified edit distance, usually 1 or 2
WORDS_BY_EDITDISTANCE_FILE = PROJ_BASE_DIR + "words_by_editdistance"
    
# File with list of all stems used in mail body, on a unique-basis
STEMS_FILE = PROJ_BASE_DIR + "stems"

# File with a list of top words in the collection, along with its
# frequency in absolute numbers.
TOPWORDS_FILE = PROJ_BASE_DIR + "topwords"

# For each (increasingly alphabetical ordered stem) hold the tf*idf
# values on a per-document basis -- one document per line
# (in increasingly alphabetical order of the document's name)
TFIDF_MATRIX = PROJ_BASE_DIR + "tfidf_stems_matrix"

# Path to the directory with the input data in XML format 
# (as of now: only FITUG-mails)
MAIL_FOLDER_XML = PROJ_BASE_DIR + "fitug_xml" + sep

# Path to mail folder with all messages delimited by '\n' (for each 
# content unit)
MAIL_FOLDER_LINE = PROJ_BASE_DIR + "fitug_line" + sep

# Nouns file, containing nouns, found at the Apertium project:
# "http://apertium.svn.sourceforge.net/viewvc/apertium/incubator/
# apertium-de-en/"
NOUNS_FILE = PROJ_RES_DIR + "nouns.txt"

# This file is used to hold SHA512 hash sums of different generated
# material, in order to avoid generating files over and over again,
# and to allow for reusing material w/o the need for regeneration.
HASH_FILE = PROJ_BASE_DIR + "hashsums"

# This file is a bidictionary from the Apertium Free RBMT system from 
# the German to English language, used here to increase relatedness 
# between words. This file is held in an XML format.
DE_EN_BIDIX_FILE = PROJ_RES_DIR + "apertium-de-en.de-en.dix"

# This file contains synsets; derived from the OpenThesaurus project
SYNSETS_FILE = PROJ_RES_DIR + "openthesaurus.txt"

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