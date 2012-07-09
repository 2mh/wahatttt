#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
Based upon (public domain) source, at URL:
http://code.activestate.com/recipes/52256-check-xml-well-formedness/
@author Paul Prescod (http://code.activestate.com/recipes/users/11203/)
@author Hernani Marques <h2m@access.uzh.ch>, 2012 (some adaptions)
"""
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.dom.minidom import Document as Doc
from glob import glob
from collections import defaultdict
from sys import argv
from codecs import open
from re import sub
from wh4t.settings import printOwnInfo
from wh4t.settings import getDefaultEncoding
from wh4t.settings import getInvalidXmlFileName
from wh4t.settings import getMailFolder

printOwnInfo(__file__)

invalidXmlFileHandler = open(getInvalidXmlFileName(),
"w",getDefaultEncoding())
invalidXmlDoc = Doc()
invalidColl = invalidXmlDoc.createElement("invalidCollection")
invalidXmlDoc.appendChild(invalidColl)
invalidStat = defaultdict(int)

def addInvalidDocs(fileName, excStr):
    invalidDoc = invalidXmlDoc.createElement("invalidDocument")
    invalidFileName = invalidXmlDoc.createTextNode(fileName)
    errStr = sub(fileName+":","",excStr)
    invalidDoc.setAttribute("error",errStr)
    invalidDoc.appendChild(invalidFileName)
    invalidColl.appendChild(invalidDoc)
    invalidStat[sub("[0-9:]*\s","",errStr)] += 1

def parseFile(fileName):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(fileName)

if len(argv) == 1:
    argv.append(getMailFolder() + "*")

for arg in argv[1:]:
    for fileName in glob(arg):
        try:
            parseFile(fileName)
            # print "%s is well-formed" % fileName
        except Exception, e:
            # print "%s is NOT well-formed! %s" % (fileName, e)
            addInvalidDocs(fileName, str(e))
            print fileName
            continue

for err,no in invalidStat.items():
    print err+" : "+str(no)
invalidXmlFileHandler.write(invalidXmlDoc.toprettyxml())
invalidXmlFileHandler.close()
if len(invalidStat.values()) == 0:
    print "No XML errors found in " + getMailFolder()
else:
    print "XML file with detailed error info written to " \
        +getInvalidXmlFileName()
