#!/bin/sh
# @author Hernani Marques <h2m@access.uzh.ch>, 2012
# UN*X Pipeline to get the (pure) German nouns out of the apertium de-en bidix 
# file.
grep -E "<l>[[:upper:]]+.*<s n=\"n\"" apertium-de-en.de-en.dix | 
cut -d ">" -f2 |
html2text -utf8 | 
sed -e "s|^ ||" | 
sed -e "s| |\n|g" | 
sort -u > nouns.txt
