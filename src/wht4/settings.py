#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from os import getcwd
from os import sep
from os.path import basename
from os.path import join
from os.path import abspath
from re import sub

"""
Global constants
DEFAULT_ENCODING: Ensure everything's using one encoding only (here: UTF-8)
MAIL_FOLDER_BASENAME: OS-Independent Foldername in CWD of the project
MAIL_FOLDER: Folder containing original text in XML format
INVALID_XML_FILE: XML file containg info about broken XML files
MAILBODY_RAW_FILE: Simple text file with all (body) content available, raw
MAILBODY_LIN_FILE: Simple text file with all (body) content available, linguistic data only
MAILBODY_SYMBOLS_FILE: List of all symbols used in mail body
MAILBODY_STEMS_FILE: List of all stems used in mail body
VERSION: Version of the wahatttt system as a whole; as of 1.0 it'll be usable
"""

DEFAULT_ENCODING = "utf-8"
WHT4_BASEDIR = abspath("..")+sep
INVALID_XML_FILE_NAME = WHT4_BASEDIR + "wht4invalidXml.xml"
MAILBODY_RAW_FILE = WHT4_BASEDIR + "mailBodyRawFile.txt"
MAILBODY_LIN_FILE = WHT4_BASEDIR + "mailBodyLinFile.txt"
MAILBODY_SYMBOLS_FILE = WHT4_BASEDIR + "mailBodySymbolsFile.txt"
MAILBODY_TOKENS_FILE = WHT4_BASEDIR + "mailBodyTokensFile.txt"
MAILBODY_TYPES_FILE = WHT4_BASEDIR + "mailBodyTypesFile.txt"
MAILBODY_TYPES_LOWERED_FILE = WHT4_BASEDIR + "mailBodyTypesLoweredFile.txt"
MAILBODY_WORDS_FILE = WHT4_BASEDIR + "mailBodyWordsFile.txt"
MAILBODY_STEMS_FILE = WHT4_BASEDIR + "mailBodyStemsFile.txt"
MAIL_FOLDER_BASENAME = WHT4_BASEDIR + "fitug_xml"
MAIL_FOLDER = join(getcwd(),MAIL_FOLDER_BASENAME)+sep
VERSION = "0.1"

# Helper functions
def print72(): print 72*"*"

def printOK(): print(" -- OK")

def getOwnInfo(callingFile):
    progName = sub(".py","",basename(callingFile))
    infoStr = "wahatttt"+" v"+VERSION+" - "+sub("wht4","",progName)
    return infoStr

def printOwnInfo(callingFile): 
    print72()
    print getOwnInfo(callingFile)
    print72()
    
def getMailFolder(): return MAIL_FOLDER

def getInvalidXmlFileName(): return INVALID_XML_FILE_NAME

def getDefaultEncoding(): return DEFAULT_ENCODING

def getMailBodyRawFile(): return MAILBODY_RAW_FILE

def getMailBodyLinFile(): return MAILBODY_LIN_FILE()

def getMailBodySymbolsFile(): return MAILBODY_SYMBOLS_FILE

def getWht4BaseDir(): return WHT4_BASEDIR

def getMailBodyTokensFile(): return MAILBODY_TOKENS_FILE

def getMailBodyTypesFile(lower=False): 
    if lower == False:
        return MAILBODY_TYPES_FILE
    return MAILBODY_TYPES_LOWERED_FILE

def getMailBodyWordsFile(): return MAILBODY_WORDS_FILE

def getMailBodyStemsFile(): return MAILBODY_STEMS_FILE

def getBaseDir(): return WHT4_BASEDIR
