#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Arian Sanusi <arian@sanusi.de>, 2012
@author Hernani Marques <h2m@access.uzh.ch>, 2012 (some adaptions)
"""

class listByLen(list):    
    def __getitem__(self,length):
        """returns [ i for i in self if len(i) == length ]"""
        
        return listByLen( ( i for i in self if len(i) == length ) )
        
    def __getslice__(self,start,end):
        
        a = listByLen()
        for length in range(start,end+1):
            a.extend(self[length])
        return a

""" How to use?
import listByLen
regularList = list(["a","wuff","miau","yeah","koffer","hamsterföderation","hamsterföderative"])
print regularList

newList = listByLen(regularList)[1:4]
print newList
['a', 'wuff', 'miau', 'yeah', 'koffer', 'hamsterf\xc3\xb6deration', 'hamsterf\xc3\xb6derative']
['a', 'wuff', 'miau', 'yeah']
"""