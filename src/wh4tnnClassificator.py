#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from codecs import open

from nltk.text import Text, TextCollection
from progressbar import ProgressBar as progressbar

# from kluster.pca import Pca # To be removed eventually

from wh4t.settings import printOwnInfo, getMailBodyStemsFile, \
                          getDefaultEncoding
from wh4t.documents import collection
from wh4t.library import dict_from_file
from atom import Text

def main():
    """ 
    This program is a start to do text classification upon the 
    "Hebbian Principal Compontent Clustering" neuronal method, as proposed by 
    Niederberger/Stoop/Christen/Ott in 2012.
    For sample source code (available under the BSDL), look at the project
    machine learning scripts, available at: 
    https://github.com/IAS-ZHAW/machine_learning_scripts
    """
    printOwnInfo(__file__)
    
    # Read all text in
    xmlCollection = collection()
    nltkTextCollectionList = list()
    
    print "Creating NLTK text collection ... "
    xmlCollectionList = xmlCollection.getDocs()
    pb = progressbar(maxval=len(xmlCollectionList)).start()
    cnt = 0
    for doc in xmlCollectionList:
        cnt += 1
        pb.update(cnt)
        nltkTextCollectionList.append(list(doc.getStems()))
    nltkTextCollection = TextCollection(nltkTextCollectionList)
    
    print "Calculating idf values for all stems ..."
    allStems = xmlCollection.getDocsStems(uniq=True)
    idfSet = set()
    pb = progressbar(maxval=len(allStems)).start()
    cnt = 0
    for word in allStems:
        cnt += 1
        pb.update(cnt)
        idf = nltkTextCollection.idf(word)
        if idf > 0.0: 
            idfSet.add((idf, word))
    
    f = open(getMailBodyStemsFile(measure="_idf"), "w",
             getDefaultEncoding())
    for pair in sorted(idfSet, reverse=True): 
        f.write(pair[1] + " " + str(pair[0]) + "\n")
    f.close()
     
    idf_dict = dict_from_file(getMailBodyStemsFile(measure="_idf"))
    
    for doc in xmlCollection.getDocs():
        nltkTextCollection = TextCollection(Text(doc.getStems()))
    
    """ To be removed eventually
    # Do primary component analysis on all raw material & show it visually
    pca = Pca()
    d = getMailFolder(contentFormat="line")
    for line_file in listdir(d)[:42]: # For now only a subset can be processed
        pca.load_line(d + line_file)
    pca.show()
    """
    
    # XXX: To be continued ...
    
if __name__ == "__main__":
    main()