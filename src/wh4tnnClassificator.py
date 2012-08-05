#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from os import listdir

from kluster.pca import Pca

from wh4t.settings import printOwnInfo, getMailFolder
from wh4t.documents import collection

def main():
    """ 
    This program is a start to do text classification upon the 
    "Hebbian Principal Compontent Clustering" neuronal method, as proposed by 
    Niederberger/Stoop/Christen/Ott in 2012.
    For sample source code (available under the GPL v3), look at the project
    "kluster" at github: https://github.com/Niederb/kluster
    """
    printOwnInfo(__file__)
    
    # Read all text in
    xmlCollection = collection()
    
    # Write it in raw format
    xmlCollection.writeRawText()
    
    # Do primary component analysis on all raw material & show it visually
    pca = Pca()
    d = getMailFolder(contentFormat="line")
    for line_file in listdir(d)[:42]: # For now only a subset can be processed
        pca.load_line(d + line_file)
    pca.show()
    
    # XXX: To be continued ...
    
if __name__ == "__main__":
    main()