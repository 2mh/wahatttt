#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
Some parts heavily based upon code (under the BSDL) available here:
* https://github.com/IAS-ZHAW/machine_learning_scripts/
  blob/master/src/ml/atizo/atizo_clustering_sim.py
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from codecs import open
from os.path import exists
import random
import colorsys

from nltk.text import TextCollection
from progressbar import ProgressBar as progressbar
from matplotlib.pyplot import figure, ion, title, scatter, draw, gcf, np

# from kluster.pca import Pca # To be removed eventually
from kluster.util import decay_learning_rate, const_learning_rate
from kluster.hebbian_clustering import project_items, learn_weights
from wh4t.settings import printOwnInfo, getMailBodyStemsFile, \
                          getDefaultEncoding
from wh4t.documents import collection
from wh4t.library import dict_from_file
from wh4t.settings import get_tfidf_matrix_file
from wh4t.settings import getDefaultNumberOfClusters

def get_nltk_text_collection(xmlCollection):
    """
    @param xmlCollection: A collection of all (as of now) XML documents,
                          of type collection.
    @return: Retrieves an NLTK TextCollection with all stems from our 
             document collection.
    """
    nltkTextCollectionList = list()
    
    print "Creating NLTK text collection ... "
    xmlCollectionList = xmlCollection.getDocs()
    
    pb = progressbar(maxval=len(xmlCollectionList)).start()
    cnt = 0
    for doc in xmlCollectionList:
        cnt += 1
        pb.update(cnt)
        nltkTextCollectionList.append(list(doc.getStems()))
        
    return TextCollection(nltkTextCollectionList)

def write_tfidf_file(xmlCollection, nltkTextCollection):
    """
    Writes a tf*idf matrix file with all tf*idf values for each document,
    row by row. The columns represent the (alphabetically ordered) stems
    available in the whole collection.
    @param xmlCollection: Collection of XML documents, type collection
    @param nltkTextCollection: NLTK TextCollection of all the stems
    """
    idf_file =  getMailBodyStemsFile(measure="_idf")
    
    if not exists(idf_file):
        write_idf_file(xmlCollection, nltkTextCollection)

    idf_dict = dict_from_file(idf_file)
    
    f = open(get_tfidf_matrix_file(), "w", getDefaultEncoding())
    for doc in xmlCollection.getDocs():
        docStems = doc.getStems()
        col = TextCollection("")
       
        print doc.getId()
        idf_row = ""
        for docStem in sorted(xmlCollection.getDocsStems(uniq=True)):
            tf = col.tf(docStem, docStems)
            idf_row += str(tf*float(idf_dict[docStem])) + " "
        f.write(idf_row + "\n")
    f.close()
    
def write_idf_file(xmlCollection, nltkTextCollection):
    """
    Writes a (collection-wide) file with idf valus for each stem.
    @param xmlCollection: Collection of XML documents, type collection
    @param nltkTextCollection: NLTK TextCollection of all the stems
    """
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
    


def iterate(data, n_clusters, n_visual_dimensions, indices):
    # n_records = data.shape[0]
    data = data / 4
    data = data - np.mean(data, 0)
    
    fig = figure(1, figsize=(14, 8))
    subplot = fig.add_subplot(111)
    
    #learning_rate = decay_learning_rate(1.0, 500.0, 0.0010)
    learning_rate = decay_learning_rate(1.0, 500.0, 0.010)
    visual_learning_rate = const_learning_rate(0.0001)    
    #W = np.random.randn(n_records, n_features)
    W = None
    W_subgroups = [None for i in range(n_clusters)]
    
    ion()
    color_values = np.random.rand(n_clusters)
    colors = np.zeros((n_clusters, 3))
    for i in range(n_clusters):
        colors[i] = colorsys.hsv_to_rgb(color_values[i], 1.0, 1.0)
    
    learn_iterations = 1000
    iterations = 10
    for i in xrange(iterations):
        #item_index = int((n_records-20)/iterations*i)+20
        #learn_data = data[0:item_index, :] #simulate a growing dataset
        learn_data = data

        (W, W_subgroups) = learn_weights(learn_data, W, W_subgroups, n_clusters, learn_iterations, learning_rate, visual_learning_rate)
        (x, y, cluster_mapping) = project_items(learn_data, W, W_subgroups, indices)
        #rescale "circle" visualization
        visual_location = np.zeros((learn_data.shape[0], n_visual_dimensions))
        visual_location[:, 0] = 500 + 300 * x
        visual_location[:, 1] = 700 + 300 * y
        
        title('PCA')
        #plot(range(len(singular_values)), np.sqrt(singular_values))
        fig.delaxes(subplot)
        subplot = fig.add_subplot(111)
        scatter(np.array(np.real(visual_location[:, 0])), np.array(np.real(visual_location[:, 1])), c=colors[cluster_mapping, :])
        subplot.axis([0, 1200, 0, 1200])
        draw()
        canvas = gcf().canvas
        canvas.start_event_loop(timeout=0.010)
    
def process_project(tfidf_file):
    tfidf_matrix = np.genfromtxt(tfidf_file, delimiter=' ')
    
    print "TF*IDF matrix: "
    print tfidf_matrix
    n_clusters = getDefaultNumberOfClusters()
    n_visual_dimension = tfidf_matrix.shape[1]
    
    indices = range(tfidf_matrix.shape[0])
    random.shuffle(indices)
    rand_data = tfidf_matrix[indices, :]
    
    iterate(rand_data, n_clusters, n_visual_dimension, indices)

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
    
    # XXX: Better check with hashsums (to avoid corrupted content)
    if not exists(get_tfidf_matrix_file()):
        nltkTextCollection = get_nltk_text_collection(xmlCollection)
        write_tfidf_file(xmlCollection, nltkTextCollection)
        print "TF*IDF matrix written to: ", get_tfidf_matrix_file()
    else:
        print "TF*IDF matrix seems available: ", get_tfidf_matrix_file()
        
    # XXX: Classification code follows here.
    process_project(get_tfidf_matrix_file())
    
    """ To be removed eventually
    # Do primary component analysis on all raw material & show it visually
    pca = Pca()
    d = getMailFolder(contentFormat="line")
    for line_file in listdir(d)[:42]: # For now only a subset can be processed
        pca.load_line(d + line_file)
    pca.show()
    """
    
if __name__ == "__main__":
    main()