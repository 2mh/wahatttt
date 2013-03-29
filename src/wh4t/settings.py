# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012-2013
"""
import datetime as t
from os import sep
from os.path import basename, abspath, join, pardir, curdir
from re import sub

################
# Default values
################

# Version of the wahatttt system as a whole; as of 1.0 it'll be usable
VERSION = "0.9"

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
DEFAULT_IDF_FILTER_VALUE = 3

# Number of terms which must match in order to cluster two documents.
# With a number of 5 (empirically tested) for ~99% of the documents a
# cluster with at least two documents can be constructed, i. e. if
# DEFAULT_IDF_FILTER_VALUE = 2.0. If higher, then much less is possible,
# as more frequent terms get removed.
DEFAULT_COMMON_TERMS_NUMBER = 300

# Name the graph for web visualization has
DEFAULT_GRAPH_NAME = "wh4t_graph"

# Standard resolution for the web graph in the browser, width x height
DEFAULT_WEBGRAPH_RESOLUTION = (960, 500)

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

# Directory for visualized web output
WEB_OUTPUT_DIR = PROJ_BASE_DIR + "wh4t_web" + sep

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