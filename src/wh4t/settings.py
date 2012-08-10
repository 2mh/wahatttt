#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from os import sep
from os.path import basename, abspath, join, pardir, curdir
from re import sub

################
# Default values
################

# Ensure everything's using one encoding only (here: UTF-8).
DEFAULT_ENCODING = "UTF-8"

# The number of top words (by frequency) displayed / written when 
# not further specified. This is used in different contexts.
DEFAULT_NUMBER_OF_TOP_WORDS = 42

# This int is the default number for how long source words used to check
# against others -- by the measure of edit distance -- should be. 0 is 
# implemented to mean "of any length".
DEFAULT_SOURCE_WORD_LEN_FOR_EDIT_DISTANCING = 0

# That's the default suffix a filename with word pairs in within some edit 
# distance contains.
DEFAULT_EDIT_DISTANCE_FILENAME_SUFFIX = ""

# Number of clusters to create (for now used for the neuronal clustering)
DEFAULT_NUMBER_OF_CLUSTERS = 4

##########################
# Paths to folders / files
##########################

# The project's base path relative to the position of this settings file.
WH4T_BASE_DIR = abspath(join(curdir, pardir)) + sep

# The project's (freely available linguistic) resources directory
WH4T_RES_DIR = WH4T_BASE_DIR + "resources" + sep

# A directory where words are hold, per document; file by file
WH4T_WORDS_DIR = WH4T_BASE_DIR + "words" + sep

# A directory where nouns are hold, per document; file by file
WH4T_NOUNS_DIR = WH4T_BASE_DIR + "nouns" + sep

# XML file containing info about broken XML files, if any (hopefully not).
INVALID_XML_FILE_NAME = WH4T_BASE_DIR + "wh4tinvalidXml.xml"

# Text file with all (body) content available, in raw form.
MAILBODY_RAW_FILE = WH4T_BASE_DIR + "mailBodyRawFile"

# Text file with all (body) content available, linguistic data only,
# achieved after some cleaning
MAILBODY_LIN_FILE = WH4T_BASE_DIR + "mailBodyLinFile"

# Text file with list of all symbols used in the mail body
MAILBODY_SYMBOLS_FILE = WH4T_BASE_DIR + "mailBodySymbolsFile"

# File with list of all tokens used, from the raw text (in the given order)
MAILBODY_TOKENS_FILE = WH4T_BASE_DIR + "mailBodyTokensFile"

# File with list of all unique tokens (=types) used
MAILBODY_TYPES_FILE = WH4T_BASE_DIR + "mailBodyTypesFile"

# File with list of all unique tokens used in lowered form
MAILBODY_TYPES_LOWERED_FILE = WH4T_BASE_DIR + "mailBodyTypesLoweredFile"

# File with list of all words (= cleaned tokens), in the given order
MAILBODY_WORDS_FILE = WH4T_BASE_DIR + "mailBodyWordsFile"

# File with nouns in the collection, is a subset of nouns.
MAILBODY_NOUNS_FILE = WH4T_BASE_DIR + "mailBodyNouns"

# File with pairs of words by a specified edit distance, usually 1 or 2
MAILBODY_WORDS_BY_EDIT_DISTANCE_FILE = WH4T_BASE_DIR + \
    "mailBodyWordsByEditDistance"
    
# File with list of all stems used in mail body, on a unique-basis
MAILBODY_STEMS_FILE = WH4T_BASE_DIR + "mailBodyStemsFile"

# File with a list of top words in the collection, along with its frequency 
# in absolute numbers.
MAILBODY_TOP_WORDS_FILE = WH4T_BASE_DIR + "mailBodyTopWordsFile"

# For each (increasingly alphabetical ordered stem) hold the tf*idf values
# on a per-document basis -- one document per line (in increasingly
# alphabetical order of the document's name)
TFIDF_MATRIX = WH4T_BASE_DIR + "tfidf_stems_matrix"

# Path to the directory with the input data in XML format 
# (as of now: only FITUG-mails)
MAIL_FOLDER_XML = WH4T_BASE_DIR + "fitug_xml" + sep

# Path to mail folder with all messages delimited by '\n' (for each content
# unit)
MAIL_FOLDER_LINE = WH4T_BASE_DIR + "fitug_line" + sep

# Nouns file, containing nouns, found at the Apertium project:
# "http://apertium.svn.sourceforge.net/viewvc/apertium/incubator/
# apertium-de-en/"
NOUNS_FILE = WH4T_RES_DIR + "nouns.txt"

# This file is used to hold SHA512 hash sums of different generated material, 
# in order to avoid generating files over and over again, and to allow for
# reusing material w/o the need for regeneration.
HASH_FILE = WH4T_BASE_DIR + "hashsums.txt"

# Version of the wahatttt system as a whole; as of 1.0 it'll be usable
VERSION = "0.5"

#################
# General getters
#################

def getOwnInfo(callingFile):
    """
    @return: A string indicating this software package, the filename --
             specific to the calling file object -- and the version number.
    """
    progName = sub(".py", "", basename(callingFile))
    infoStr = "wahatttt" + " v" + VERSION+" - " + sub("wh4t", "", progName)
    return infoStr

def getDefaultNumberOfTopWords():
    """
    @return: The number of top words set by default used when at some
             point top words by frequency are displayed / written.
    """
    return DEFAULT_NUMBER_OF_TOP_WORDS

def getDefaultEditDistanceFilenameSuffix():
    """
    @return: Defined suffix when not specified 
    """
    return DEFAULT_EDIT_DISTANCE_FILENAME_SUFFIX

def getDefaultSourceWordLenForEditDistancing():
    """
    @return: Default int number for queries being made by edit distance.
    """
    return DEFAULT_SOURCE_WORD_LEN_FOR_EDIT_DISTANCING

def getDefaultNumberOfClusters():
    """
    @return: Returns number of clusters to create
    """
    return DEFAULT_NUMBER_OF_CLUSTERS

##########################################################################
# Getters for file names, needed in other classes, to read or write files.
# See definitions section for more information on its intended content.
##########################################################################
    
def getMailFolder(contentFormat="XML"): 
    """
    @param: If type's "CSV" return mail folder where mails in CSV format 
            lie
    @return: String with mail folder path of the input data
    """
    if contentFormat == "line":
        return MAIL_FOLDER_LINE
    
    # Fallback case "XML"
    return MAIL_FOLDER_XML

def getWordsFolder(pos='_'):
    """
    @param: If pos is 'n' return a path to store nouns, otherwise to store
            words in general.
    @return: Return a path as string to store words by document
    """
    if (pos == 'n'): 
        return WH4T_NOUNS_DIR
    # Default
    return WH4T_WORDS_DIR

def getInvalidXmlFileName(): 
    """
    @return: String to a file path for invalid XML documents
    """
    return INVALID_XML_FILE_NAME

def getDefaultEncoding(): 
    """
    @return: String of the default encoding engaged
    """
    return DEFAULT_ENCODING

def getMailBodyRawFile(): 
    """
    @return: String with path to a file for all the raw content
    """
    return MAILBODY_RAW_FILE

def getMailBodyLinFile(): 
    """
    @return: String with path to a file for all the linguistic content
    """
    return MAILBODY_LIN_FILE()

def getMailBodySymbolsFile(): 
    """
    @return: String to a file for storing all the symbols used
    """
    return MAILBODY_SYMBOLS_FILE

def getWh4tBaseDir(): 
    """
    @return: String with path for the project's main/root directory
    """
    return WH4T_BASE_DIR

def getMailBodyTokensFile(): 
    """
    @return: String with file path for holding the tokens in use
    """
    return MAILBODY_TOKENS_FILE

def getMailBodyTypesFile(lower=False):
    """
    @param lower: Indicate if tokens file shall contain only lower case
                  letters (=True), otherwise file shall be in mixed cases
    @return: String with file path to the file feat. types (=unique tokens),
                  either mixed or only lower cased
    """ 
    if lower == False:
        return MAILBODY_TYPES_FILE
    return MAILBODY_TYPES_LOWERED_FILE

def getMailBodyWordsFile(pos='_'): 
    """
    @param pos: When '_' all words, when 'n' nouns file
    @return: String with file path where found words are written to 
    """
    if (pos == 'n'):
        return MAILBODY_NOUNS_FILE
    
    return MAILBODY_WORDS_FILE

def getMailBodyStemsFile(measure=""): 
    """
    @pos measure: If a special measure is saved in this file. Something that
                  makes sense to be stored along with the nouns is their 
                  "IDF" values.
    @return: String with file path to hold the unique stems encountered
             (along with other info)
    """
    return MAILBODY_STEMS_FILE + measure

def getMailBodyWordsByEditDistanceFile(
    editDistance=getDefaultEditDistanceFilenameSuffix()):
    """
    @param: Positive integer specifying of which edit distance the word
            pairs are
    @return: String with file path to store pairs of words edit-distanced 
             by a specified length
    """
    fileName = MAILBODY_WORDS_BY_EDIT_DISTANCE_FILE
    return fileName + str(editDistance)

def getMailBodyTopWordsFile(): 
    """
    @return: String with file path to store the most frequent words
    """
    return MAILBODY_TOP_WORDS_FILE

def getNounsFile(measure=""):
    """
    @return: String with file path to store nouns
    """
    return NOUNS_FILE + measure

def getHashFile():
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

###################################
# Simple printer / helper functions
###################################

def printLine(): 
    """
    To create semi-graphical lines used to seperate output on the terminal
    """
    print 78*"*"

def printOK(): 
    """
    To indicate on the terminal something went OK, e. g. creation of a file
    """
    print(" -- OK")
    
def printOwnInfo(callingFile):
    """
    Prints information about the file that includes and uses this
    function to the terminal.
    @param: Object of the file we want information about, usually the
            calling file.
    """
    printLine() 
    print getOwnInfo(callingFile)
    printLine()