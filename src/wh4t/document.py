#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from os.path import getsize
from xml.etree import cElementTree as ET

class document(dict):
    """
    The class document is used to represent the individual documents,
    which are to be classified by wh4t.
    For the time being these documents are e-mail messages from the
    FTIUG debate@ mailing list.

    This class is a dict -- it parses the XML files and stores all of its 
    values in terms of key-value-pairs.
    """
    
    ############################################################
    # Attributes parsed
    # - The only (important) attributes used are mail id numbers
    #############################################################
    
    MAIL_TAG_ID_ATTR = "id"
    IN_REPLY_TO_TAG_ID_ATTR = MAIL_TAG_ID_ATTR
    
    #######################################################################
    # Tags parsed
    # - Tags used include such as <subj>, <author> or <content> (text body)
    #######################################################################

    MAIL_TAG = "mail" # containing id attrib
    URL_TAG = "url" # mail resource at http location, in HTML
    SUBJ_TAG = "subj"
    AUTHOR_TAG = "author"
    EMAIL_TAG = "email"
    DATE_TAG = "date" # saved in format: "%a, %d %b, %Y %H:%M:%S" (~ RFC2822)
    REF_TAG = "references"  # for <references> in <mail>, 
                            # containing <inReplyto>
    IN_REPLY_TO_TAG = "inReplyTo"
    CONTENT_TAG = "content"
    
    #################################################################
    # Other key names, for now for storing the xml filename
    #################################################################
    
    XML_FILEPATH = "file"
    
    ###################################
    # The object gets instantiated here
    ###################################
    
    def __init__(self, xmlFilePath):
        """
        @param xmlFilePath: The path to the xml file we want to parse
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
        # - However, thus who do have, do have -- ATM -- one reference only.
        xmlRefElem = xmlMailElem.find(self.REF_TAG)
        
        # Check for existence of <references>
        # At the end: Store id attribute of <inReplyToTag> in object 
        # itself, if the <references> tag does, in fact, exit.
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
        
    def getXmlFileName(self): 
        """
        @return: The full absolute path to the XML file represented
                 in this object.
        """
        return self[self.XML_FILEPATH]
    
    ############################################################
    # Getters for the values stored in an instance of this class
    ############################################################
    
    def getId(self): 
        """
        @return: String with mail id
        """
        return self[self.MAIL_TAG]
    
    def getUrl(self): 
        """
        @return: String with url pointing to the web,
                 where the original mail (in HTML) can be found
        """
        return self[self.URL_TAG]
    
    def getSubj(self): 
        """
        @return: String with mail subject
        """
        return self[self.SUBJ_TAG]
    
    def getAuthor(self): 
        """
        @return: String with sender's name
        """
        return self[self.AUTHOR_TAG]
    
    def getEmail(self): 
        """
        @return: String with the e-mail address;
                 it may contain the name again
        """
        return self[self.EMAIL_TAG]
        
    def getDate(self): 
        """
        @return: String with the date in a standardized
                 notation
        """
        return self[self.DATE_TAG]
    
    def getInReplyToId(self): 
        """
        @return: String with mail id of the message this document
                 is referring to; caution: may be None, e. g. if
                 this document is the start of a thread and is thus
                 not in reply to another one
        """
        return self[self.IN_REPLY_TO_TAG] 
    
    def getRawContent(self): 
        """
        @return: String with the raw content -- as originally found
                 in <content>
        """
        return self[self.CONTENT_TAG]
    
    #################################################################
    # Other getters, not relying on data in an instance of this class
    #################################################################
    
    def getFileSize(self):
        """
        @return: Return integer with file size of the xml document
        """
        return getsize(self.getXmlFileName())
    
    def getRawLen(self): 
        """
        @return: Returns raw content as string, which originally 
                 was found in <content> node
        """
        return len(self.getRawContent())
    
    ##########################################
    # Methods to print content to the terminal
    ##########################################
    
    def printRawContent(self): 
        """
        Print the <content> part of the message to the terminal. 
        """        
        print self[self.CONTENT_TAG]
