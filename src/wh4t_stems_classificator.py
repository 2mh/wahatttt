#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from wh4t.documents import Collection
from wh4t.library import exists_tfidf_matrix, get_positional_index
from wh4t.settings import print_own_info, get_tfidf_matrix_file, \
                          get_def_common_terms_no

def process_project(tfidf_matrix_file, xmlcollection):
    """
    Here starts the classification upon the TF*IDF matrix.
    """
    pos_idx = get_positional_index(tfidf_matrix_file)
    no_of_docs = len(xmlcollection.get_docs())
    doc_cluster_pairs = list()
    
    doc_idx1 = 0
    max_doc_idx = no_of_docs - 1
    for doc_line1 in pos_idx:
        doc_idx2 = doc_idx1 + 1 # Do comparison as of next document
        terms1 = set(doc_line1)
        common_terms = set()
        
        # Last document doesn't have other document to compare to;
        # break loop
        if(doc_idx1 == max_doc_idx):
            break
        
        while True:
            terms2 = set(pos_idx[doc_idx2])
            common_terms= terms1.intersection(terms2)
            
            # Break loop if last document reached to compare to
            if(doc_idx2 == max_doc_idx):
                break
            
            if len(common_terms) >= get_def_common_terms_no():
                doc_no1 = doc_idx1 + 1
                doc_no2 = doc_idx2 + 1
                clustered_doc_pair = [doc_no1, doc_no2]
                doc_cluster_pairs.append([clustered_doc_pair, common_terms])
            
            doc_idx2 += 1
                 
        doc_idx1 += 1
             
    # XXX: To remove; show cluster pairs built     
    print len(doc_cluster_pairs)
    set_of_docs_clustered = set()
    for pair in doc_cluster_pairs:
        print pair
        set_of_docs_clustered.add(pair[0][0])
        set_of_docs_clustered.add(pair[0][1])
    rate_of_docs_clustered = float(len(set_of_docs_clustered)) / no_of_docs
    print "Number of docs clustered:", len(set_of_docs_clustered), "/", \
                                       no_of_docs
    print "Rate of docs clustered:", rate_of_docs_clustered
        
def main():
    """
    Here starts a classificator which makes categorization upon certain 
    stems.
    """
    print_own_info(__file__)
    
    xmlcollection = Collection()
    
    if exists_tfidf_matrix(xmlcollection, create=True) is True:
        process_project(get_tfidf_matrix_file(), xmlcollection)
    
if __name__ == "__main__":
    main()