#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""
from xml.etree import cElementTree as ET
from os.path import getsize

class document(dict):
    """
    The class document is used to represent the individual documents,
    which are to be classified by wh4t.
    For the time being these documents are e-mail messages from the
    FTIUG debate@ mailing list.

    This class is a dict -- it parses the XML files and stores all of its 
    values in terms of key-value-pairs.
    """
    
    # The only (important) attributes used are mail id numbers
    MAIL_TAG_ID_ATTR = "id"
    IN_REPLY_TO_TAG_ID_ATTR = MAIL_TAG_ID_ATTR
    
    # Tags used include such as <subj>, <author> or <content> (text body)
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
        """
        Upon initialization all the tags and (important) attributes are
        read and stored in the object's itself (is a dict).
        """
        self[self.XML_FILEPATH] = xmlFilePath
        xmlFileHandler = ET.parse(xmlFilePath)
        
        # Get <mail> node
        xmlMailElem = xmlFileHandler.find(self.MAIL_TAG)
        
        # Store id attribute of <mail>
        self[self.MAIL_TAG] = xmlMailElem.get(self.MAIL_TAG_ID_ATTR)
   
        # Store text of <url> tag
        self[self.URL_TAG] = xmlMailElem.find(self.URL_TAG).text    
         
        # Store text of <subj> tag
        self[self.SUBJ_TAG] = xmlMailElem.find(self.SUBJ_TAG).text
        
        # Store text of <author> tag
        self[self.AUTHOR_TAG] = xmlMailElem.find(self.AUTHOR_TAG).text
        
        # Store text of <email> tag
        self[self.EMAIL_TAG] = xmlMailElem.find(self.EMAIL_TAG).text
        
        # Store text of <date> tag
        self[self.DATE_TAG] = xmlMailElem.find(self.DATE_TAG).text
        
        
        # Get id from mail in <inReplyTo> tag, but:
        # - Not all mails have its parent: <references>
        # - However, thus wo have, do have -- ATM -- one reference only.
        
        xmlRefElem = xmlMailElem.find(self.REF_TAG)
        
        # Check for existence of <references>
        # At the end: Store id attricbute of <inReplyToTag> in object 
        # itself, if the <references> tag does, in fact, exit
        if (xmlRefElem) == None:
            self[self.IN_REPLY_TO_TAG] = None
        else:
            xmlInReplyToElem = \
            xmlMailElem.find(self.REF_TAG).find(self.IN_REPLY_TO_TAG)
        
            self[self.IN_REPLY_TO_TAG] = \
            xmlInReplyToElem.get(self.IN_REPLY_TO_TAG_ID_ATTR)
        
        # Store text of <content> tag (=mail body) 
        self[self.CONTENT_TAG] = \
            xmlFileHandler.find(self.CONTENT_TAG).text        
        
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
