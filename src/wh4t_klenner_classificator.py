#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Basically based upon code from Manfred Klenner <klenner@cl.uzh.ch>, 2012
Some adaptions made by Hernani Marques <h2m@access.uzh.ch>, 2012
"""

import re
import numpy as np
import sys
sys.path[0] = \
    '/home/klenner/Desktop/Lehre/dist_semantics/nimfa/palermo/pymf-read-only/lib'
import pymf
import scipy
import scipy.io

thresline=500000     # wieviele Zeilen aus vso.ngram_new
threshold=2000       # wieviele Nomen, Dimension der Matrix
rankval=10           # wieviele Klassen
iterval=50

file='vso.ngram_new'

# verbs=['sagen','hoffen','glauben']

# read lines from dewac tripels (z.B. haben Haus Fenster=221)
def wacex(File):
    p=re.compile('\|(.*)') # Haus|Hus|... --> Haus
    z=re.compile('(\d+)')  # fetch frequency
    q=re.compile('=(\d+)') # remove =frequency
    vs={}
    c=0
    for line in open(file):   #codecs.open(file, "r", "utf-8" ):  #open(file):
        (verb,subj,obj)=line.split()
#    if not verb in verbs: continue
        c+=1
        if c > thresline: break
        subj=p.sub('',subj)
        freq=int(z.search(obj).group())
        obj=p.sub('',obj)
        obj=q.sub('',obj)
        if vs.has_key(verb): vs[verb].append((subj,obj,freq))
        else: vs[verb]=[(subj,obj,freq)]
    return vs  # hash with verbs as index and subj-obj-freq-tripel as values

vs=wacex(file)

# wie oft kommt subj-obj mit irgendeinem Verb vor: hsv[(subj,obj)]+=freq
# wie oft kommt subj bzw. obj vor: x[subj]+=freq etc.
x={}
y={}
hsv={}
for verb in vs.keys():
    sv=0
    ov=0
    for (subj,obj,freq) in vs[verb]:
        if hsv.has_key((subj,obj)): hsv[(subj,obj)]+=freq
        else: hsv[(subj,obj)]=freq
        if x.has_key(subj): x[subj]+=freq
        else: x[subj]=freq
        if y.has_key(obj): y[obj]+=freq
        else: y[obj]=freq

# nimm nur die n häufigsten Nomen
# man könnte auch 2 thresholds einführen für n x m Matrix
c=0
sk=[]
ok=[]
for obj in reversed(sorted(y,key=lambda obj:y[obj])):
    if c> threshold: break
    c+=1
    sk.append(obj)
c=0
for subj in reversed(sorted(x,key=lambda subj:x[subj])):
    if c> threshold: break
    c+=1
    ok.append(subj)

# generiere Matrix mit n x n Dimensionen
V=np.zeros((len(sk),len(ok)),float)

# schreibe die Häufigkeiten in die Zellen
for (subj,obj) in hsv.keys():
    if subj in sk and obj in ok:
        V[sk.index(subj),ok.index(obj)]=hsv[(subj,obj)]

# faktorisiere
print "**** Imatrize"
def cluster(V,sk):
    global rankval, iterval
    lclass={}

    nmf_mdl=pymf.NMF(V,num_bases=rankval,niter=iterval)
    nmf_mdl.factorize()
# initialisiere die Klassen
    for xclass in range(0,rankval):
        lclass[xclass]=[]
# weise jeder Klasse alle seinen Mitglieder zu
# Kriterium: höchster Wert
    for noun in sk:
        myclass=-1
        myprob=-1
        for xclass in range(0,rankval):
            if nmf_mdl.W[sk.index(noun),xclass] > myprob:
                myclass=xclass
                myprob=nmf_mdl.W[sk.index(noun),xclass]
        lclass[myclass].append(noun)

    # ausgeben der Klassen
    for xclass in range(0,rankval):
        print lclass[xclass]

# subj-obj: obj-dimension wird auf rankval reduziert
cluster(V,sk)