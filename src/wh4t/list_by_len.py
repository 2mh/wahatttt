# -*- coding: utf-8 -*-
"""
@author Arian Sanusi <arian@sanusi.de>, 2012
@author Hernani Marques <h2m@access.uzh.ch>, 2012 (some adaptions)
"""

class ListByLen(list):
    """    
    It's used like the following:
    from list_by_len import ListByLen
    regularlist = list(["a","wuff","miau","yeah","koffer",
                        "hamsterföderation","hamsterföderative"])
    print regularlist
    ['a', 'wuff', 'miau', 'yeah', 'koffer', 'hamsterf\xc3\xb6deration',
     'hamsterf\xc3\xb6derative']

    newlist = ListByLen(regularlist)[1:4]
    print newlist
    ['a', 'wuff', 'miau', 'yeah']
    """    
    def __getitem__(self, length):
        """
        @return: [ i for i in self if len(i) == length]
        """ 
        return ListByLen( ( i for i in self if len(i) == length ) )
        
    def __getslice__(self, start, end):
        """
        @param start: Start of subset of list we want.
        @param end: End of subset of list we want.
        @return: List (subset) from a given start to the end.
        """   
        a = ListByLen()
        for length in range(start, end + 1):
            a.extend(self[length])
        return a
