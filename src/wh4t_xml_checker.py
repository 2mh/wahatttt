#! /usr/bin/env python2.7
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

from wh4t.settings import print_own_info, get_def_enc, \
                          get_invalid_xml_filename, get_mailfolder

print_own_info(__file__)

def add_invalid_docs(filename, exceptstring):
    """
    Add invalid documents by filename and exception string to the above
    prepared file.
    @param filename: String of Filename of the invalid XML document 
                     found.
    @param exceptstring: Exception string that lead to an error, including
                   the position where the error was found.
    """
    invalid_doc = invalid_xmldoc.createElement("invalid_document")
    invalid_doc_filename = invalid_xmldoc.createTextNode(filename)
    errstring = sub(filename + ":", "", exceptstring)
    invalid_doc.setAttribute("error", errstring)
    invalid_doc.appendChild(invalid_doc_filename)
    invalid_xmldocs.appendChild(invalid_doc)
    invalidstat[sub("[0-9:]*\s", "", errstring)] += 1

def parseFile(filename):
    """
    Parse XML document by filename
    """
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(filename)

# Program starts here
# Throughpass all documents in globally defined mail folder 
# (=input XML docs)
if len(argv) == 1:
    argv.append(get_mailfolder() + "*")
for arg in argv[1:]:
    for filename in glob(arg):
        # If works, document is well-formed
        try:
            parseFile(filename)
        # If exception occurs, document is not well-formed; add to 
        # collection of invalid docs.
        except Exception, e:
            add_invalid_docs(filename, str(e))
            print filename
            continue
        
# Prepare XML file to write invalid input XML files of the
# collection into.
invalid_xml_filehandler = open(get_invalid_xml_filename(), "w", get_def_enc())
invalid_xmldoc = Doc()
invalid_xmldocs = invalid_xmldoc.createElement("invalid_xmldocsection")
invalid_xmldoc.appendChild(invalid_xmldocs)
invalidstat = defaultdict(int)

# Check collection of invalid docs and effectively write XML
# invalid file.
for err, no in invalidstat.items():
    print err + " : " + str(no)
invalid_xml_filehandler.write(invalid_xmldoc.toprettyxml())
invalid_xml_filehandler.close()
if len(invalidstat.values()) == 0:
    print "No XML errors found in " + get_mailfolder()
else:
    print "XML file with detailed error info written to " \
        + get_invalid_xml_filename()