#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2013
"""  

"""
TODO:
1. 
Make program parametrizable, e. g. possibility to indicate YAML file.
2.
...
"""

import matplotlib.pyplot as plt
import networkx as nx
from nltk.metrics import jaccard_distance
from os.path import exists
from progressbar import ProgressBar

from d3_js import d3_js
from wh4t.documents import Collection
from wh4t.library import get_def_graph_name, get_graph_file, \
                         print_own_info
 
def main():
    print_own_info(__file__)

    yaml_file = get_graph_file()
    if exists(yaml_file):
        print "Graph (YAML) file exists: ", yaml_file
        print "Reading it ..."
        g = nx.read_yaml(yaml_file)
        d3_js.export_d3_js(g)
        print "Web files exported: ", 
    else:
        create_graph()


def create_graph():  
    g = nx.Graph()
    print "Loading collection ..."
    xml_docs = Collection()
    docs_no = xml_docs.get_docs_no()
    id_dict = dict()
    stems_dict = dict()
    doc_id = 1
    
    print "Put stems into a dict for each document (with an uniq id) ..."
    print "Create nodes with all the documents' relevant information ..."
    pb = ProgressBar(maxval=docs_no).start()
    for xml_doc in xml_docs.get_docs():
        pb.update(doc_id)
        id_dict[xml_doc.get_xml_filename()] = doc_id
        g.add_node(doc_id, 
                   id = xml_doc.get_id(),
                   rawlen = xml_doc.get_rawlen(),
                   subj = xml_doc.get_subj(),
                   author = xml_doc.get_author(),
                   date = xml_doc.get_date(),
                   words = xml_doc.get_words()[:10],
                   uniq_stems = list(xml_doc.get_stems(uniq=True))[:10],
                   rawcontent = xml_doc.get_rawcontent()
                   )
        doc_id += 1
        stems_dict[doc_id] = xml_doc.get_stems(uniq=True)
        
    print "Create undirected, weighted graph based on Jaccard similarity ..."
    no_of_edges = docs_no * (docs_no - 1) / 2
    pb = ProgressBar(maxval=no_of_edges).start()
    count = 1
    for doc_idx1 in stems_dict.keys():
        doc_idx2 = doc_idx1 + 1
        # Nothing left to compare
        if (doc_idx1 == docs_no):
            break
    
        while True:
            # print "Comparing: ", doc_idx1, doc_idx2
            
            # Find longer doc
            doc1_len, doc2_len = len(stems_dict[doc_idx1]), \
                                    len(stems_dict[doc_idx2])
            long_doc_len = max((doc1_len, doc2_len))
            short_doc_len = min((doc1_len, doc2_len))
            alias_coeff = float(long_doc_len) / short_doc_len
            
            edge_weight = (1 - jaccard_distance(stems_dict[doc_idx1],
                                           stems_dict[doc_idx2])) \
                           * alias_coeff
            print alias_coeff, edge_weight
            
            # To be made more flexible
            if edge_weight == 1:
                g.add_edge(doc_idx1, doc_idx2, weight=edge_weight)
            doc_idx2 += 1
            pb.update(count)
            count += 1
            if doc_idx2 > docs_no:
                break
    
    print "Draw graph showing possible clusters  ..."
    
    elarge = [(u,v) for (u,v,d) in g.edges(data=True) if d['weight'] > 0.4]
    emedium = [(u,v) for (u,v,d) in g.edges(data=True) 
              if d['weight'] > 0.2 and d['weight'] < 0.4]
    esmall = [(u,v) for (u,v,d) in g.edges(data=True) if d['weight'] <= 0.2]
    print "elarge: ", len(elarge)
    print "emedium: ", len(emedium)
    print "esmall: ", len(esmall)
       
    pos = nx.spring_layout(g, scale=20)
    #pos = nx.random_layout(g)
    
    dlarge = [n for n,d in g.degree_iter() if d >= 20]
    dmedium = [n for n,d in g.degree_iter() if d > 1 and d < 20]
    dsmall = [n for n,d in g.degree_iter() if d == 1]
    dnone = [n for n,d in g.degree_iter() if d == 0]
    print "dlarge: ", len(dlarge)
    print "dmedium: ", len(dmedium)
    print "dsmall: ", len(dsmall)
    print "dnone: ", len(dnone)
    
    # Draw nodes
    # nx.draw_networkx_nodes(g, pos, node_size=5, linewidths=0)
    nx.draw_networkx_nodes(g, pos, nodelist=dlarge, node_size=20,
                           node_color='b',
                           linewidths=0)
    nx.draw_networkx_nodes(g, pos, nodelist=dmedium, node_size=10,
                           node_color='g',
                           alpha=0.8, 
                           linewidths=0)
    nx.draw_networkx_nodes(g, pos, nodelist=dsmall, node_size=5,
                           node_color='b',
                           alpha=0.2,
                           linewidths=0,
                           )
    nx.draw_networkx_nodes(g, pos, nodelist=dnone, node_size=5,
                           node_color='b',
                           alpha=0.2, 
                           linewidths=0)
    
    # Draw edges
    nx.draw_networkx_edges(g, pos, edgelist=elarge, width=0.4)
    nx.draw_networkx_edges(g, pos, edgelist=emedium, edge_color='g', 
                           alpha=0.8, width=0.2)
    nx.draw_networkx_edges(g, pos, edgelist=esmall, width=0.1,
                           alpha=0.1, edge_color='b')
    
    # Draw labels
    # nx.draw_networkx_labels(g, pos, font_size=1, font_family='sans-serif')
    
    plt.axis('off')
    plt.figure(1, figsize=(20,20))
    """
    print "Print PNG"
    plt.savefig("graph.png", dpi=600)
    """
    # plt.show()
    nx.write_yaml(g, get_graph_file())
    d3_js.export_d3_js(g)
    
    #import d3_js
    #g = nx.read_yaml("../test_mit_name.yaml")

if __name__ == "__main__":
    main()