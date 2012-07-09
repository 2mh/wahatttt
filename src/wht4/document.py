#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from xml.etree import cElementTree as ET
from os.path import getsize

class document(dict):
    
    """ XXX: Interesting problem (python v2.6.6):
        - If I put all the fields not into this class (is dict) itself, but into
          a dictionary of this class, data gets lost during processing ...
          E. g. for the use of a class-internal dict, which loses data:
          (1) mail = {}; # Before __init__
          (2) self.mail[self.XML_FILEPATH] = xmlFilePath # In __init__
        - WTF? To investigate later.
    """
    
    """
    Fields to parse and save in mail dict, containing
    - tags
    - some attributes
    """
    
    # the only (important) attributes used are mail id numbers
    MAIL_TAG_ID_ATTR = "id"
    IN_REPLY_TO_TAG_ID_ATTR = MAIL_TAG_ID_ATTR
    
    # tags
    XML_FILEPATH = "file"
    MAIL_TAG = "mail" # containing id attrib
    URL_TAG = "url" # mail resource at http location, in HTML
    SUBJ_TAG = "subj"
    AUTHOR_TAG = "author"
    EMAIL_TAG = "email"
    DATE_TAG = "date" # saved in format: "%a, %d %b, %Y %H:%M:%S" (~ RFC2822)
    REF_TAG = "references" # for <references> in <mail>, containing <inReplyto>
    IN_REPLY_TO_TAG = "inReplyTo"
    CONTENT_TAG = "content"
    
    def __init__(self,xmlFilePath):
        self[self.XML_FILEPATH] = xmlFilePath
        xmlFileHandler = ET.parse(xmlFilePath)
        
        # Go through <mail>
        xmlMailElem = xmlFileHandler.find(self.MAIL_TAG)
        
        # Get id
        self[self.MAIL_TAG] = xmlMailElem.get(self.MAIL_TAG_ID_ATTR)
   
        # Get url
        self[self.URL_TAG] = xmlMailElem.find(self.URL_TAG).text    
         
        # Get subject
        self[self.SUBJ_TAG] = xmlMailElem.find(self.SUBJ_TAG).text
        
        # Get author
        self[self.AUTHOR_TAG] = xmlMailElem.find(self.AUTHOR_TAG).text
        
        # Get e-mail
        self[self.EMAIL_TAG] = xmlMailElem.find(self.EMAIL_TAG).text
        
        # Get date
        self[self.DATE_TAG] = xmlMailElem.find(self.DATE_TAG).text
        
        """
        Get id from mail in reply to, but:
        - not all mails have references
        - thus wo have, do have -- ATM -- one reference only
        """
        xmlRefElem = xmlMailElem.find(self.REF_TAG)
        
        if (xmlRefElem) == None:
            self[self.IN_REPLY_TO_TAG] = None
        else:
            xmlInReplyToElem = \
            xmlMailElem.find(self.REF_TAG).find(self.IN_REPLY_TO_TAG)
        
            self[self.IN_REPLY_TO_TAG] = \
            xmlInReplyToElem.get(self.IN_REPLY_TO_TAG_ID_ATTR)
        
        # Get mail text
        self[self.CONTENT_TAG] = \
            xmlFileHandler.find(self.CONTENT_TAG).text
            
        self[self.CONTENT_TAG] = xmlFileHandler.find(self.CONTENT_TAG).text
        
        self.text = xmlFileHandler.find(self.CONTENT_TAG).text
        
        self[self.CONTENT_TAG] = self.text
        
        
    # Return xml file name (/w path)
    def getXmlFileName(self): return self[self.XML_FILEPATH]
    
    # Getters for all information found in the 
    def getId(self): return self[self.MAIL_TAG]
    
    def getUrl(self): return self[self.URL_TAG]
    
    def getSubj(self): return self[self.SUBJ_TAG]
    
    def getAuthor(self): return self[self.AUTHOR_TAG]
    
    def getEmail(self): return self[self.EMAIL_TAG]
    
    def getDate(self): return self[self.DATE_TAG]
    
    # May return None, if the message is not in reply to another one
    def getInReplyToId(self): return self[self.IN_REPLY_TO_TAG]
    
    def getRawContent(self):
        """
        data would get lost (only occasionally!) 
        doing the following (using a dict -- mail -- of this class):
        return self.mail[self.CONTENT_TAG]
        """
        return self[self.CONTENT_TAG]
    
    # Other getters
    def getFileSize(self): 
        return getsize(self.getXmlFileName())
    
    def getRawLen(self): return len(self.getRawContent())
    
    # Other methods
    def printRawContent(self): print self[self.CONTENT_TAG]
