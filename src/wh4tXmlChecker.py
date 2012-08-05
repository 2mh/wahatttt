#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
Based upon (public domain) source, at URL:
http://code.activestate.com/recipes/52256-check-xml-well-formedness/
@author Paul Prescod (http://code.activestate.com/recipes/users/11203/)
@author Hernani Marques <h2m@access.uzh.ch>, 2012 (some adaptions)
"""

from glob import glob
from collections import defaultdict
from sys import argv
from codecs import open
from re import sub

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.dom.minidom import Document as Doc

from wh4t.settings import printOwnInfo, getDefaultEncoding, \
                          getInvalidXmlFileName, getMailFolder

printOwnInfo(__file__)

def addInvalidDocs(fileName, excStr):
    """
    Add invalid documents by fileName and exception string to the above
    prepared file.
    @param fileName: String of Filename of the invalid XML document found.
    @param excStr: Exception string that lead to an error, including the
                   position where the error was found.
    """
    invalidDoc = invalidXmlDoc.createElement("invalidDocument")
    invalidFileName = invalidXmlDoc.createTextNode(fileName)
    errStr = sub(fileName + ":", "", excStr)
    invalidDoc.setAttribute("error", errStr)
    invalidDoc.appendChild(invalidFileName)
    invalidColl.appendChild(invalidDoc)
    invalidStat[sub("[0-9:]*\s", "", errStr)] += 1

def parseFile(fileName):
    """
    Parse XML document by filename
    """
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(fileName)

# Program starts here
# Throughpass all documents in globally defined mail folder (=input XML docs)
if len(argv) == 1:
    argv.append(getMailFolder() + "*")
for arg in argv[1:]:
    for fileName in glob(arg):
        # If works, document is well-formed
        try:
            parseFile(fileName)
        # If exception occurs, document is not well-formed; add to collection
        # of invalid docs.
        except Exception, e:
            addInvalidDocs(fileName, str(e))
            print fileName
            continue
        
# Prepare XML file to write invalid input XML files of the collection into.
invalidXmlFileHandler = open(getInvalidXmlFileName(), "w",
                             getDefaultEncoding())
invalidXmlDoc = Doc()
invalidColl = invalidXmlDoc.createElement("invalidCollection")
invalidXmlDoc.appendChild(invalidColl)
invalidStat = defaultdict(int)

# Check collection of invalid docs and effectively write XML invalid file.
for err, no in invalidStat.items():
    print err + " : " + str(no)
invalidXmlFileHandler.write(invalidXmlDoc.toprettyxml())
invalidXmlFileHandler.close()
if len(invalidStat.values()) == 0:
    print "No XML errors found in " + getMailFolder()
else:
    print "XML file with detailed error info written to " \
        + getInvalidXmlFileName()