#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from class_of_dict_classes import ClassOfDictClasses

testobj = ClassOfDictClasses()

testobj.write_out_var_file()
testobj.write_out_dynamic_var_in_dict_file()
testobj.write_out_static_var_in_dict_file()
testobj.write_out_var_in_class_dict_file()

print "Check the created out_* text files."