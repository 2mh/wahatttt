#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from progressbar import ProgressBar

from wh4t.documents import Collection
from wh4t.exception import VoidStructureError
from wh4t.library import exists_tfidf_matrix, get_positional_index, \
                         filter_subsets
from wh4t.settings import print_own_info, get_tfidf_matrix_file, \
                          get_def_common_terms_no, print_line, \
                          get_def_idf_filter_val
    
def create_hard_clusters(soft_clusters, no_of_docs):
    """
    
    """
    if len(soft_clusters) == 0 or no_of_docs == 0:
        raise VoidStructureError, \
        "Please provide non-zero/empty values."
    hard_clusters = list()
    border_docs = set()
    
    for s_cluster in soft_clusters:
        hard_clusters.append(s_cluster)
    
    no_clusters = len(hard_clusters)
    max_idx = no_clusters - 1
    idx1 = 0
    for cluster1 in hard_clusters:
        
        # No more element to compare to
        if idx1 == max_idx:
            break
        
        idx2 = idx1 + 1
        while True:
            
            # Last element already processed
            if idx2 == no_clusters:
                break
            
            # Continuously save document numbers which happen to appear
            # in more than one cluster alone
            border_docs = border_docs.union(set(cluster1[0]).
                                        intersection(hard_clusters[idx2][0]))
            idx2 += 1
        
        idx1 += 1

    hard_clusters_tmp = hard_clusters
    hard_clusters = list()
    for h_cluster in hard_clusters_tmp:
        h_cluster[0] = list(set(h_cluster[0]).difference(border_docs))
        hard_clusters.append(h_cluster)
    
    # XXX / Caution: Associated terms not cleaned accordingly
    return hard_clusters 

def create_soft_clusters(doc_cluster_pairs):
    """
    Caution: May become deprecated
    
    @param doc_cluster_pairs: Pairs clustered together 
    
    Transitively create soft-bordered cluster groups, which can be
    used to "see" which documents belong semantically -- 
    directly or indirectly -- together. Use for that the clustered
    pairs.
    Problem: There are documents ("vertices") which belong to several
             clusters, which may be indicators of a topic shift.
    
    """
    soft_clusters = list()
    paths_list = list()
    no_of_cluster_pairs = len(doc_cluster_pairs)
    
    max_doc_pair_idx = no_of_cluster_pairs - 1
    doc_pair_idx1 = 0
    print "Making out soft clusters ... may take a while."
    pb = ProgressBar(maxval=no_of_cluster_pairs).start()
    for doc_pair, _ in doc_cluster_pairs:
        doc_pair1 = set(doc_pair)
        path_vertices = doc_pair1
        doc_pair_idx2 = doc_pair_idx1 + 1
        
        # No more paths to find if maximum index is reached
        if (doc_pair_idx1 == max_doc_pair_idx):
            break
        
        while True:        
            # Last element reached before; break loop
            if(doc_pair_idx2 == max_doc_pair_idx):
                break
            
            doc_pair2 = set(doc_cluster_pairs[doc_pair_idx2][0])           
            # If there's a path to a pair, add it to the vertices' list
            if len(path_vertices.intersection(doc_pair2)) == 1:
                path_vertices = path_vertices.union(doc_pair2)
                     
            doc_pair_idx2 += 1
        
        path = tuple(sorted(path_vertices))
        paths_list.append(path)
        
        # Remove duplicates and subsets
        # => remove paths fully or partly contained in other paths
        paths_list = filter_subsets(paths_list)
            
        doc_pair_idx1 += 1
        pb.update(doc_pair_idx1)   
    
    # XXX: To be put into seperate function.
    print "\n", "Number of unique paths found:", len(paths_list)
    for path in paths_list:
        print path
    
    return soft_clusters
    
def print_clusters(clusters, no_of_docs):
    """
    
    Prints documents by their numbers they were clustered together
    because of common terms. Also shows how many documents could be
    clustered.
    
    @param clusters: A list containing document numbers
                    clustered together upon a certain number
                    of common terms (represented by their
                    numbers, too).
    @param no_of_docs: The number (int) of documents the collection we
                       clustered consists of.
                       
    """
    if len(clusters) == 0 or no_of_docs == 0:
        raise VoidStructureError, \
        "Please provide non-zero/empty values."
    
    set_of_docs_clustered = set()
    cluster_sizes = list()
    
    for docs, _ in clusters:
        cluster_sizes.append(len(docs))
        for doc in docs:
            set_of_docs_clustered.add(doc)
    cluster_sizes = sorted(cluster_sizes)
    
    rate_of_docs_clustered = float(len(set_of_docs_clustered)) / no_of_docs
    print "Lowest IDF value considered for terms:", \
          get_def_idf_filter_val()
    print "Number of feature terms used to cluster:", \
          get_def_common_terms_no() 
    print "Number of clusters built:", len(clusters)
     
    print "Number of docs clustered:", len(set_of_docs_clustered), "/", \
                                       no_of_docs
    print "Average cluster size:", \
        sum(cluster_sizes) / float(len(cluster_sizes))
    print "Median cluster size:", cluster_sizes[len(cluster_sizes)/2]
    ten_biggest_clusters = sorted(cluster_sizes, reverse=True)[:10]
    print "Ten biggest cluster sizes:", ten_biggest_clusters
    print "Coverage of ten biggest clusters over docs clustered:", \
        sum(ten_biggest_clusters) / float(len(set_of_docs_clustered))
    print "Rate of docs clustered:", rate_of_docs_clustered

def process_project(tfidf_matrix_file, xmlcollection):
    """
    Here starts the classification upon the TF*IDF matrix.
    """
    pos_idx = get_positional_index(tfidf_matrix_file)
    no_of_docs = len(xmlcollection.get_docs())
    cluster_pairs = list() # In here create cluster pairs
    soft_clusters = list() # In here create soft clusters
    
    doc_idx1 = 0
    max_doc_idx = no_of_docs - 1
    for doc_line1 in pos_idx:
        doc_idx2 = doc_idx1 + 1 # Do comparison as of next document
        terms1 = set(doc_line1)
        common_terms = set()
        soft_cluster = set()
        soft_cluster_common_terms = set()
        
        # Last document doesn't have other document to compare to;
        # break loop
        if(doc_idx1 == max_doc_idx):
            break
        
        already_added = False
        while True:
            # Break loop if last document reached to compare to
            # already reached before
            if(doc_idx2 == max_doc_idx):
                break
            
            terms2 = set(pos_idx[doc_idx2])
            common_terms = terms1.intersection(terms2)
            soft_cluster_common_terms = \
                soft_cluster_common_terms.union(common_terms)
            
            if len(common_terms) >= get_def_common_terms_no():
                doc_no1 = doc_idx1 + 1
                doc_no2 = doc_idx2 + 1
                clustered_doc_pair = [doc_no1, doc_no2]
                
                if already_added == False:
                    soft_cluster.add(doc_no1)
                    already_added = True
                soft_cluster.add(doc_no2)

                cluster_pairs.append([clustered_doc_pair, common_terms])
            
            doc_idx2 += 1
           
        if len(soft_cluster) > 0:
            soft_clusters.append([tuple(sorted(soft_cluster)), 
                                  tuple(sorted(soft_cluster_common_terms))])  
            
        doc_idx1 += 1
        
    # Print found cluster pairs
    # print_clusters(cluster_pairs, no_of_docs)
    print_line()
    soft_clusters = filter_subsets(soft_clusters, nested=True)
    print "Soft clustering (statistics): "
    print_clusters(soft_clusters, no_of_docs)
    print_line()
    print "Hard clustering (statistics): "
    hard_clusters = create_hard_clusters(soft_clusters, no_of_docs)
    print_clusters(hard_clusters, no_of_docs)
    # Create distinct clusters from pairs; pairs may overlap 
    # / may be transitive
    # soft_clusters = create_soft_clusters(doc_cluster_pairs)
        
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