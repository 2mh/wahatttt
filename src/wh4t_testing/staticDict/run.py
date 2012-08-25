#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from classOfDictClasses import classOfDictClasses

testObj = classOfDictClasses()

testObj.writeOutVarFile()
testObj.writeOutDynamicVarInDictFile()
testObj.writeOutStaticVarInDictFile()
testObj.writeOutVarInClassDictFile()

print "Check your *.txt files."