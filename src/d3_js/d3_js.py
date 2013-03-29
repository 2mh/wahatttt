#! /usr/bin/env python2.7
# encoding: utf-8
"""
d3_js.py

Description: Read and write files in the D3.js JSON file format.  This
can be used to generate interactive Java Script embeds from NetworkX
graph objects.

These functions will read and write the D3.js JavaScript Object Notation (JSON)
format for a graph object. There is also a function to write write HTML and Javascript 
files need to render force-directed layout of graph object in a browser.  The default
redering options are based on the force-directed example by Mike Bostock at
(http://mbostock.github.com/d3/ex/force.html).

Created by Drew Conway (drew.conway@nyu.edu) on 2011-07-13 
Extended by Hernani Marques (h2m@access.uzh.ch) in 2013
# Copyright (c) 2011, 2013 under the Simplified BSD License.  
# For more information on the BSD license see: 
# http://www.opensource.org/licenses/bsd-license.php
# All rights reserved.
"""

"""
TODO (Priority 1):
1.
Size of graph in wh4t_graph.js must be set optimally (dynamically?)
2.
distance & charge must be adjusted in a way, that interaction w/
graph is useful
3a.
Field update functionality should be created dynamically
3b.
Code should be much more flexible (create subfunctions or similar)

TODO (Priority 2):
1.
Zoom functionality is still broken; must be fixed
"""

__author__=["""Drew Conway (drew.conway@nyu.edu)""",
		    """Hernani Marques (h2m@access.uzh.ch)"""]

__all__=['write_d3_js',
		 'd3_json',
		 'export_d3_js']

import os
import sys
from shutil import copyfile
#from networkx.utils import _get_fh
from networkx.utils import make_str
import networkx as nx
import json
import re	

from wh4t.library import get_def_enc, get_def_graph_name, \
						 get_web_output_dir, get_webgraph_res

d3_html = '''<!DOCTYPE html>
<html>
  <head>
    <title>wh4t webgraph</title>
    <script type="text/javascript" src="d3/d3.v2.js" charset="UTF-8"></script>
    <link type="text/css" rel="stylesheet" href="d3/force.css"/>
  </head>
  <body>
  <script type="text/javascript" src="wz/wz_tooltip.js"></script> 
        <table border="1" width="100%">
        <tr>
        <td>
    <div id="chart"></div>
        </td>
        <td width="30%">
        <table height="500">
        <tr><td height="50"><h2>Doc: &nbsp;</h2></td><td><div id="doc_no"></div></td></tr>
        <tr><td height="50"><h2>Group:&nbsp;</h2></td><td><div id="group_no"></div></td></tr>
        <tr><td height="200"><h2>Stems:&nbsp;</h2></td><td><div id="stems"></div></td></tr>
        <tr><td height="200"><h2>Words:&nbsp;</h2></td><td><div id="words"></div></td></tr>
        </tr>
        </table>
        </td>
        </tr>
        </table>
    <script type="text/javascript" src="wh4t_graph.js"></script>
  </body>
</html>
'''

def is_string_like(obj): # from John Hunter, types-free version
    """Check if obj is string."""
    try:
        obj + ''
    except (TypeError, ValueError):
        return False
    return True

def _get_fh(path, mode='r'):
    """ Return a file handle for given path.

Path can be a string or a file handle.

Attempt to uncompress/compress files ending in '.gz' and '.bz2'.

"""
    if is_string_like(path):
        if path.endswith('.gz'):
            import gzip
            fh = gzip.open(path,mode=mode)
        elif path.endswith('.bz2'):
            import bz2
            fh = bz2.BZ2File(path,mode=mode)
        else:
            fh = open(path,mode = mode)
    elif hasattr(path, 'read'):
        fh = path
    else:
        raise ValueError('path must be a string or file handle')
    return fh

def write_d3_js(G, path, group=None, encoding="utf-8"):
	"""Writes a NetworkX graph in D3.js JSON graph format to disk.
	
	Parameters
	----------
	G : graph
		a NetworkX graph
	path : file or string
       File or filename to write. If a file is provided, it must be
       opened in 'wb' mode. Filenames ending in .gz or .bz2 will be compressed.
	group : string, optional
		The name 'group' key for each node in the graph. This is used to 
		assign nodes to exclusive partitions, and for node coloring if visualizing.
	encoding: string, optional
       Specify which encoding to use when writing file.
		
	Examples
	--------
	>>> from networkx.readwrite import d3_js
	>>> G = nx.path_graph(4)
	>>> G.add_nodes_from(map(lambda i: (i, {'group': i}), G.nodes()))
	>>> d3_js.write_d3_js(G, 'four_color_line.json')
	"""
	fh = _get_fh(path, 'wb')
	graph_json = d3_json(G, group)
	graph_dump = json.dumps(graph_json, indent=2)
	fh.write(graph_dump.encode(encoding))
	

def d3_json(G, group=None):
	"""Converts a NetworkX Graph to a properly D3.js JSON formatted dictionary
	
	Parameters
	----------
	G : graph
		a NetworkX graph
	group : string, optional
		The name 'group' key for each node in the graph. This is used to 
		assign nodes to exclusive partitions, and for node coloring if visualizing.
		
	Examples
	--------
	>>> from networkx.readwrite import d3_js
	>>> G = nx.path_graph(4)
	>>> G.add_nodes_from(map(lambda i: (i, {'group': i}), G.nodes()))
	>>> d3_js.d3_json(G)
	{'links': [{'source': 0, 'target': 1, 'value': 1},
	  {'source': 1, 'target': 2, 'value': 1},
	  {'source': 2, 'target': 3, 'value': 1}],
	 'nodes': [{'group': 0, 'nodeName': 0},
	  {'group': 1, 'nodeName': 1},
	  {'group': 2, 'nodeName': 2},
	  {'group': 3, 'nodeName': 3}]}
	"""
	ints_graph = nx.convert_node_labels_to_integers(G, discard_old_labels=False)
	graph_nodes = ints_graph.nodes(data=True)
	graph_edges = ints_graph.edges(data=True)
	
	node_labels = [(b,a) for (a,b) in ints_graph.node_labels.items()]
	node_labels.sort()
	
	# Build up node dictionary in JSON format
	if group is None:
		graph_json = {'nodes': map(lambda n: {'name': str(node_labels[n][1]), 'group' : 0}, xrange(len(node_labels)))}
	else:
		try:
			graph_json = {'nodes' : map(lambda n: {'name': str(node_labels[n][1]), 'group' : graph_nodes[n][1][group]}, xrange(len(node_labels)))}
		except KeyError:
			raise nx.NetworkXError("The graph had no node attribute for '"+group+"'")
	
	# Iterate through nodes
	nodes_indices = G.nodes()
	for i in nodes_indices:
		node = G.node[i]
		for key in node:
			j = i - 1
			val = node[key]
			if type(val) == set:
				val = list(val)
			graph_json['nodes'][j][key] = val
		
	# Build up edge dictionary in JSON format
	json_edges = list()
	for j, k, w in graph_edges:
		e = {'source' : j, 'target' : k}
		if any(map(lambda k: k=='weight', w.keys())):
			e['value'] = w['weight']
		else:
			e['value'] = 1
		json_edges.append(e)
	
	graph_json['links'] = json_edges
	return graph_json
	
def export_d3_js(G, 
				files_dir=get_web_output_dir(), 
				graphname=get_def_graph_name(), 
				group=None, 
				width=get_webgraph_res()[0], 
				height=get_webgraph_res()[1], 
				node_labels=False, 
				encoding=get_def_enc()):
	"""
	A function that exports a NetworkX graph as an interavtice D3.js object.  
	The function builds a folder, containing the graph's formatted JSON, the D3.js 
	JavaScript, and an HTML page to load the graph in a browser.
	
	Parameters
	----------
	G : graph
		a NetworkX graph
	files_dir : string, optional
		name of directory to save files
	graphname : string, optional
		the name of the graph being save as JSON, will appears in directory as 'graphname.json'
	group : string, optional
		The name of the 'group' key for each node in the graph. This is used to 
		assign nodes to exclusive partitions, and for node coloring if visualizing.
	width : int, optional
		width (px) of display frame for graph object in browser window
	height : int, optional
		height (px) of display frame for graph object in browser window
	node_labels : bool, optional
		If true, nodes are displayed with labels in browser
	encoding: string, optional
       Specify which encoding to use when writing file.
		
	Examples
	--------
	>>> from scipy import random
	>>> from networkx.readwrite import d3_js
	>>> G = nx.random_lobster(20, .8, .8)
	>>> low = 0
	>>> high = 5
	>>> G.add_nodes_from(map(lambda i: (i, {'group': random.random_integers(low, high, 1)[0]}), G.nodes()))
	>>> G.add_edges_from(map(lambda e: (e[0], e[1], {'weight': random.random_integers(low+1, high, 1)[0]}), G.edges()))
	>>> d3_js.export_d3_js(G, files_dir="random_lobster", graphname="random_lobster_graph", node_labels=False)
	"""
	if not os.path.exists(files_dir):
	    os.makedirs(files_dir)
	
	# Begin by creating the necessary JS and HTML files

	write_d3_js(G, path=files_dir+"/"+graphname+".json", group=group, encoding=encoding)
	
	
	graph_force_html = open(files_dir+'/'+graphname+'.html', 'w')
	for line in d3_html.split("\n"):
		if line.find('"../../d3.js"') > 0:
			line = line.replace('"../../d3.js"', '"d3/d3.js"')
		if line.find('"../../d3.geom.js"') > 0:
			line = line.replace('"../../d3.geom.js"', '"d3/d3.geom.js"')
		if line.find('"../../d3.layout.js"') > 0:
			line = line.replace('"../../d3.layout.js"', '"d3/d3.layout.js"')
		if line.find('"force.css"') > 0:
			line = line.replace('"force.css"', '"d3/force.css"')
		if line.find('"force.js"') > 0:
			line = line.replace('"force.js"', '"'+graphname+'.js"')
		graph_force_html.write(line+'\n'.encode(encoding))
	graph_force_html.close()