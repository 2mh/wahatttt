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
from sys import stdout
import random
import colorsys

from nltk.text import TextCollection
from progressbar import ProgressBar
from matplotlib.pyplot import figure, ion, title, scatter, draw, gcf, np

# from kluster.pca import Pca # To be removed eventually
from kluster.util import decay_learning_rate, const_learning_rate
from kluster.hebbian_clustering import project_items, learn_weights
from wh4t.settings import print_own_info, get_stems_file, get_def_enc
from wh4t.documents import Collection
from wh4t.library import DictFromFile
from wh4t.settings import get_tfidf_matrix_file
from wh4t.settings import get_def_no_of_clusters

def get_nltk_text_collection(xmlcollection):
    """
    @param xmlcollection: A collection of all (as of now) XML documents,
                          of type collection.
    @return: Retrieves an NLTK TextCollection with all stems from our 
             document collection.
    """
    nltk_textcollectionList = list()
    
    print "Creating NLTK text collection ... "
    xmlcollection_list = xmlcollection.get_docs()
    
    pb = ProgressBar(maxval=len(xmlcollection_list)).start()
    cnt = 0
    for doc in xmlcollection_list:
        cnt += 1
        pb.update(cnt)
        nltk_textcollectionList.append(list(doc.get_stems()))
        
    return TextCollection(nltk_textcollectionList)

def get_cluster_stems(stems, idf_dict):
    """
    This function removes most frequent and all very rare stems (single
    occurrence), to improve clustering results.
    @param stems: List of stems to be filtered
    @param idf_dict: Dictionary containing the idf values to filter
                     after
    @return: List with out-filtered stems
    """ 
    max_val = max(idf_dict.itervalues()).as_integer_ratio()
    return [stem for stem in stems
            if idf_dict[stem] > 2.0
            and not idf_dict[stem].as_integer_ratio() == max_val]

def write_tfidf_file(xmlcollection, nltk_textcollection):
    """
    Writes a tf*idf matrix file with all tf*idf values for each 
    document, row by row. The columns represent the (alphabetically
    ordered) stems available in the whole collection.
    @param xmlcollection: Collection of XML documents, type collection
    @param nltk_textcollection: NLTK TextCollection of all the stems
    """
    idf_file = get_stems_file(measure="_idf")
    avg_words_per_doc = len(xmlcollection.get_words()) / \
                        len(xmlcollection.get_docs())

    if not exists(idf_file):
        write_idf_file(xmlcollection, nltk_textcollection)

    idf_dict = DictFromFile(idf_file)
    high_tfidf_stems = set()
    
    collection_stems = list(xmlcollection.get_stems(uniq=True))
    print "Length of collection, all stems:", len(collection_stems)
    
    # Remove most frequent (idf<2) / stop stems (or qualifying 
    # as such), and most rare stems (max(idf)), as they are of no 
    # help to separate / make up clusters
    collection_stems = get_cluster_stems(collection_stems, idf_dict)
    print "Length of collection, cluster stems:", len(collection_stems)
    
    f = open(get_tfidf_matrix_file(), "w", get_def_enc())
    for doc in xmlcollection.get_docs():
        doc_stems = doc.get_stems()
        col = TextCollection("")
        
        stdout.write(doc.get_id())
        idf_row = ""
        stdout.write(" (")
        for stem in sorted(collection_stems):
            tf = col.tf(stem, doc_stems)
    
            # Reweight tf values, to get more classifcation words
            # and compensate for the very different document sizes 
            # available
            # Idea: Accounts for average document length, but also for
            # the number of times a word effictively occurs in a 
            # specific document; other variations can be thought of 
            # (using log) or maximal tf values
            # Note: The clustering works better with (in general)
            # smaller values
            if tf > 0.0:
                tf = 1.0 / avg_words_per_doc * tf
            # If nothing applies: tf is 0.0
                
            tfidf = tf*float(idf_dict[stem])
            if (tfidf > 0.0):
                stdout.write(stem + ", ")
                high_tfidf_stems.add(stem)
            idf_row += str(tfidf) + " "
        f.write(idf_row + "\n")
        stdout.write(")\n")
    f.close()
    print "List length of high value tf*idf terms:", len(high_tfidf_stems)

    
def write_idf_file(xmlcollection, nltk_textcollection):
    """
    Writes a (collection-wide) file with idf valus for each stem.
    @param xmlcollection: Collection of XML documents, type collection
    @param nltk_textcollection: NLTK TextCollection of all the stems
    """
    print "Calculating idf values for all stems ..."
    all_stems = xmlcollection.get_stems(uniq=True)
    idfset = set()
    pb = ProgressBar(maxval=len(all_stems)).start()
    cnt = 0
    for word in all_stems:
        cnt += 1
        pb.update(cnt)
        idf = nltk_textcollection.idf(word)
        if idf > 0.0: 
            idfset.add((idf, word))
    
    f = open(get_stems_file(measure="_idf"), "w", get_def_enc())
    for pair in sorted(idfset, reverse=True): 
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

        (W, W_subgroups) = learn_weights(learn_data, W, W_subgroups, 
                                         n_clusters, learn_iterations, 
                                         learning_rate, 
                                         visual_learning_rate)
        (x, y, cluster_mapping) = project_items(learn_data, W, 
                                                W_subgroups, 
                                                indices)
        #rescale "circle" visualization
        visual_location = np.zeros((learn_data.shape[0], 
                                    n_visual_dimensions))
        visual_location[:, 0] = 500 + 300 * x
        visual_location[:, 1] = 700 + 300 * y
        
        title('PCA')
        #plot(range(len(singular_values)), np.sqrt(singular_values))
        fig.delaxes(subplot)
        subplot = fig.add_subplot(111)
        scatter(np.array(np.real(visual_location[:, 0])), 
                np.array(np.real(visual_location[:, 1])), 
                c=colors[cluster_mapping, :])
        subplot.axis([0, 1200, 0, 1200])
        draw()
        canvas = gcf().canvas
        canvas.start_event_loop(timeout=0.010)
    
def process_project(tfidf_file):
    tfidf_matrix = np.genfromtxt(tfidf_file, delimiter=' ')
    
    print "TF*IDF matrix: "
    print tfidf_matrix
    n_clusters = get_def_no_of_clusters()
    n_visual_dimension = tfidf_matrix.shape[1]
    
    indices = range(tfidf_matrix.shape[0])
    random.shuffle(indices)
    rand_data = tfidf_matrix[indices, :]
    
    iterate(rand_data, n_clusters, n_visual_dimension, indices)

def main():
    """ 
    This program is a start to do text classification upon the 
    "Hebbian Principal Compontent Clustering" neuronal method,
    as proposed by  Niederberger/Stoop/Christen/Ott in 2012.
    For sample source code (available under the BSDL), look at
    the project machine learning scripts, available at: 
    https://github.com/IAS-ZHAW/machine_learning_scripts
    """
    print_own_info(__file__)
    
    # Read all text in
    xmlcollection = Collection()
    
    # XXX: Better check with hashsums (to avoid corrupted content)
    if not exists(get_tfidf_matrix_file()):
        nltk_textcollection = get_nltk_text_collection(xmlcollection)
        write_tfidf_file(xmlcollection, nltk_textcollection)
        print "TF*IDF matrix written to: ", get_tfidf_matrix_file()
    else:
        print "TF*IDF matrix seems available: ", get_tfidf_matrix_file()
        
    # Classification process starts here.
    process_project(get_tfidf_matrix_file())
    
    """ To be removed eventually
    # Do primary component analysis on all raw material & show it visually
    pca = Pca()
    d = get_mailfolder(content_format="line")
    # For now only a subset can be processed
    for line_file in listdir(d)[:42]:
        pca.load_line(d + line_file)
    pca.show()
    """
    
if __name__ == "__main__":
    main()