#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Started upon (public domain) source: http://stackoverflow.com/questions/701704/how-do-you-convert-html-entities-to-unicode-and-vice-versa-in-python
@author hekevintran (http://stackoverflow.com/users/84952/hekevintran)
@author Hernani Marques <h2m@access.uzh.ch>, June/July 2012
"""

from BeautifulSoup import BeautifulStoneSoup
from src.wh4t.settings import print_own_info

print_own_info(__file__)

"""
So far: Simply concatenates text1 to text2, returning resulting string
"""
def concattext(text1, text2): return text1 + text2

"""
Converts text with HTML entites to Unicode characters, returning Unicode string
"""
def HTMLEntitiesToUnicode(text):
    """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    return text

"""
Converts text with Umlauts to text w/o Umlauts using ASCII characters, 
Requires Unicode string as text input;
returning Unicode string
"""
def UmlautToASCII(text):
    "Converts Umlauts (UTF-8) to two-letter ASCII strings. For example 'ä' becomes 'ae'"
    retText = "" # Will become Unicode string, as text is unicode 
    for char in text:
        if char == u'ä':
    	   retText = concattext(retText, u"ae")
        elif char == u'ö':
    	   retText = concattext(retText, u"oe")
        elif char == u'ü':
    	   retText = concattext(retText, u"ue")
        else:
    	   retText = concattext(retText, u"" + char)
    return retText
    
"""
def unicodeToHTMLEntities(text):
    Converts unicode to HTML entities.  For example '&' becomes '&amp;'.
    text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
    return text
"""

text_u = "&amp;, &reg;, &lt;, &gt;, &cent;, &pound;, &yen;, &euro;, &sect;, &copy; &auml;"
text_a = u"äadfsfsafsfsaü"

uni = HTMLEntitiesToUnicode(text_u)
uml = UmlautToASCII(text_a)
# htmlent = unicodeToHTMLEntities(uni)

print uni
print uml
#print htmlent
# &, ®, <, >, ¢, £, ¥, €, §, ©
# &amp;, &#174;, &lt;, &gt;, &#162;, &#163;, &#165;, &#8364;, &#167;, &#169;
