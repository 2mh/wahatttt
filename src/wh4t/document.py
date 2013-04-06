# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from os import makedirs
from os.path import getsize, exists, basename
from collections import defaultdict
from re import match
from codecs import open

from xml.etree import cElementTree as ET
from nltk import PunktWordTokenizer as Tokenizer
from nltk.stem.snowball import GermanStemmer as Stemmer
from hashlib import sha512

from library import normalize_word, rreplace, clean_iterable, split_term, \
                    HashDict, get_mailfolder, get_def_enc, get_wordsdir, \
                    get_stemsdir, DictFromFile, get_classification_stems, \
                    get_stems_file, EnToDeDict

class document(dict):
    """
    The class document is used to represent the individual documents,
    which are to be classified by wh4t.
    For the time being these documents are e-mail messages from the
    FTIUG debate@ mailing list.

    This class is a dict -- it parses the XML files and stores all of 
    its values in terms of key-value-pairs.
    """
    
    ############################################################
    # Attributes parsed
    # - The only (important) attributes used are mail id numbers
    ############################################################
    
    MAIL_TAG_ID_ATTR = "id"
    IN_REPLY_TO_TAG_ID_ATTR = MAIL_TAG_ID_ATTR
    
    ###################################################################
    # Tags parsed
    # - Tags used include such as <subj>, <author> or <content> 
    # (text body)
    ###################################################################

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
    
    ###################################################################
    # Derived key-value pairs
    # - Derived pairs include tokenized text, stemmed text, words etc.
    ###################################################################
    
    TOKENS = "tokens"
    TYPES = "types"
    WORDS = "words"
    NOUNS = "nouns"
    STEMS = "stems"
    STEMS_UNIQ = "stems_uniq"
    WORDS_BY_EDIT_DISTANCE = "words_by_edit_distance"
    TOP_WORDS = "top_words"
    TEXT_FREQ_DIST = "text_freq_dist"
    HASHSUMS = "hashsums"
    
    ###################################################################
    # Other key names, for now for storing the xml filename, and a
    # document id
    ###################################################################
    
    XML_FILEPATH = "file"
    DOC_ID = "doc_id"
    
    ###################################
    # The object gets instantiated here
    ###################################
    
    def __init__(self, xml_filepath):
        """
        @param xml_filepath: The path to the xml file we want to parse
        Upon initialization all the tags and (important) attributes are
        read and stored in the object's itself (is a dict).
        """
        dict.__init__(self)
        
        self[self.XML_FILEPATH] = xml_filepath
        xml_file_handler = ET.parse(xml_filepath)
        
        # A document id, based on the (unique) file name
        self[self.DOC_ID] = rreplace(basename(self[self.XML_FILEPATH]),
                            ".xml", "", 1)
        
        # Populate self[self.HASHSUMS] with hashsums
        self._load_hashsums()
        
        ################################################
        # Initialize items with material directly parsed
        #################################################
        
        # Get <mail> node
        xml_mail_elem = xml_file_handler.find(self.MAIL_TAG)
        
        # Store id attribute of <mail>
        self[self.MAIL_TAG] = xml_mail_elem.get(self.MAIL_TAG_ID_ATTR)
   
        # Store text of <url> tag
        self[self.URL_TAG] = xml_mail_elem.find(self.URL_TAG).text    
         
        # Store text of <subj> tag
        self[self.SUBJ_TAG] = xml_mail_elem.find(self.SUBJ_TAG).text
        
        # Store text of <author> tag
        self[self.AUTHOR_TAG] = xml_mail_elem.find(self.AUTHOR_TAG).text
        
        # Store text of <email> tag
        self[self.EMAIL_TAG] = xml_mail_elem.find(self.EMAIL_TAG).text
        
        # Store text of <date> tag
        self[self.DATE_TAG] = xml_mail_elem.find(self.DATE_TAG).text     
        
        # Get id from mail in <inReplyTo> tag, but:
        # - Not all mails have its parent: <references>
        # - However, thus who do have, do have -- ATM -- one reference 
        #   only.
        xml_ref_elem = xml_mail_elem.find(self.REF_TAG)
        
        # Check for existence of <references>
        # At the end: Store id attribute of <inReplyToTag> in object 
        # itself, if the <references> tag does, in fact, exit.
        if xml_ref_elem is None:
            self[self.IN_REPLY_TO_TAG] = None
        else:
            xml_in_reply_to_elem = \
            xml_mail_elem.find(self.REF_TAG).find(self.IN_REPLY_TO_TAG)
        
            self[self.IN_REPLY_TO_TAG] = \
            xml_in_reply_to_elem.get(self.IN_REPLY_TO_TAG_ID_ATTR)
        
        # Store text of <content> tag (=mail body) 
        self[self.CONTENT_TAG] = \
            xml_file_handler.find(self.CONTENT_TAG).text
            
        ###############################################################
        # Initialize items for later use, like tokens, words lists/sets
        ###############################################################
        
        # For holding tokens of the text
        self[self.TOKENS] = list()
    
        # For holding types (=unique tokens)
        self[self.TYPES] = set()
        
        # For holding words (=cleaned tokens)
        self[self.WORDS] = list()
        
        # The nouns (of the words)
        self[self.NOUNS] = list()
        
        # For holding (unique) stems
        self[self.STEMS_UNIQ] = set()
        
        # For holding stems
        self[self.STEMS] = list()
        
        # For holding pairs of words distanced by some edits, in a set
        self[self.WORDS_BY_EDIT_DISTANCE] = set()
        
        # For holding the most frequent words (with absolute 
        # frequency vals)
        self[self.TOP_WORDS] = defaultdict()
        
        # For holding an object to play with the frequency 
        # distribution
        self[self.TEXT_FREQ_DIST] = None
        
    ############################################################
    # Getters for the values stored in an instance of this class
    ############################################################
    
    def get_id(self): 
        """
        @return: String with mail id
        """
        return self[self.MAIL_TAG]
    
    def get_url(self): 
        """
        @return: String with url pointing to the web,
                 where the original mail (in HTML) can be found
        """
        return self[self.URL_TAG]
    
    def get_subj(self): 
        """
        @return: String with mail subject
        """
        return self[self.SUBJ_TAG]
    
    def get_author(self): 
        """
        @return: String with sender's name
        """
        return self[self.AUTHOR_TAG]
    
    def get_email(self): 
        """
        @return: String with the e-mail address;
                 it may contain the name again
        """
        return self[self.EMAIL_TAG]
        
    def get_date(self): 
        """
        @return: String with the date in a standardized
                 notation
        """
        return self[self.DATE_TAG]
    
    def get_in_reply_to_id(self): 
        """
        @return: String with mail id of the message this document
                 is referring to; caution: may be None, e. g. if
                 this document is the start of a thread and is thus
                 not in reply to another one
        """
        return self[self.IN_REPLY_TO_TAG] 
    
    def get_rawcontent(self): 
        """
        @return: String with the raw content -- as originally found
                 in <content>
        """
        return self[self.CONTENT_TAG]
    
    def get_xml_filename(self): 
        """
        @return: The full absolute path to the XML file represented
                 in this object.
        """
        return self[self.XML_FILEPATH]
    
    def get_tokens(self):
        """
        @return: A list of all tokens found in the document; done by 
                 NLTK.
        """
        if len(self[self.TOKENS]) == 0:
            self[self.TOKENS] = Tokenizer().tokenize(self.get_rawcontent())
        return self[self.TOKENS]
    
    def get_types(self, lower=False):
        """
        @param lower: To be set to True to get only lower case types.
        @return: A set of all types (=unique tokens) found in the
                 document; create this set one time only.
        """
        if len(self[self.TYPES]) == 0:
            self[self.TYPES] = set(self.get_tokens())
        if(lower == False):
            return self[self.TYPES]
        # Lower case list and return set
        return set(map(lambda x:x.lower(), self[self.TYPES]))
    
    def get_words(self, pos='_', ref_nouns=None, trans=(False, None)):
        """
        @param pos: It's possible to say which words we want. ATM 
                    only '_' (all words; that's the default) or 'n' 
                    (nouns) are supported.
        @param ref_nouns: Optional parameter (together with pos) 
                                to indicate which reference nouns 
                                (object nouns) to use.
        @param trans: First argument specifies if translation should
                      occur; second argument gives possibility to 
                      specify a bi-dictionary as object.
        @return: Return words (determined by surface forms) that seem 
                 to be of linguistic nature, and thus "real" words.
                 Words in this sense are built out of the tokens, which 
                 also include lots of programming code in different
                 languages or other surfaces, which don't seem to be
                 natural language -- like PGP signatures or similar.
                 This construction is carried out one time only.
        XXX: This part my change heavily. Also: The regexps are ugly 
             hacks.
        """
        doc_id = self[self.DOC_ID]
        hashsums_dict = self[self.HASHSUMS]
        w, w_hash  = self.get_file(self.WORDS)
        folder = self._get_folder_by_key(self.WORDS)
        en_to_de_dict = EnToDeDict()
         
        if self[self.HASHSUMS] == 0 \
        or w_hash == None \
        or ''.join(hashsums_dict.keys()).find(folder + doc_id) < 0 \
        or not \
            w_hash == hashsums_dict[folder + doc_id]:
            
            non_word_symbol = "0123456789<>=/"
            istoadd = True
            
            if len(self[self.WORDS]) == 0:  
                for t in self.get_tokens():
                    for s in non_word_symbol:
                        if s in t:
                            istoadd = False
                            break
                    if match("[a-z]+\.[a-z]+", t) is not None \
                    or match("[ \*_\]\^\\\\!$\"\'%` ]+.*", t) is not None \
                    or match("[ &*\(\)+\#,-.:;?+\\@\[ ]+.*", t) is not None \
                    or match("[a-z]{1}-", t) is not None \
                    or t.find("--") >= 0 or t.find("..") >= 0:
                        istoadd = False             
                    if (istoadd == True):
                        # Normalize words; remove noise
                        t = normalize_word(t)
                        # Extract words from compounds; add them to list
                        if match("[a-zA-Z]+[-,.&|]+[a-zA-Z]+", t):
                            t_list = split_term(t)
                            for sub_t in t_list:
                                # Terms may become void / short; avoid 
                                # adding them
                                if len(sub_t) > 1:
                                    try: 
                                        self[self.WORDS].append(en_to_de_dict[t.lower()])
                                    except KeyError:
                                        self[self.WORDS].append(t)
                        else:
                            # As above
                            if len(t) > 1:
                                try:
                                    self[self.WORDS].append(en_to_de_dict[t.lower()])
                                except KeyError:
                                    self[self.WORDS].append(t)
                    else: # istoadd is False
                        istoadd = True
                self.write_file(self.WORDS)
        else:
            self[self.WORDS] = clean_iterable(w)
        
        # By the very first run of the system a void hashsums file gets 
        # initialized.
        # After the above code, hashsums were created => let's reflect them.
        if len(self[self.HASHSUMS]) == 0: self._load_hashsums()
            
        # Return only nouns; do it once only
        if pos == 'n' and ref_nouns is not None:
            # Approach by comparing against a nouns' list
            # and by considering words as nouns which start with
            # two upper case letters (being with high probability NEs).
            # XXX: May be possible to do faster.
            
            n, n_hash = self.get_file(self.NOUNS)
            folder = self._get_folder_by_key(self.NOUNS)
                
            if n_hash is None \
            or ''.join(hashsums_dict.keys()).find(folder + doc_id) < 0 \
            or not n_hash == \
                hashsums_dict[folder + doc_id]:
                
                if len(self[self.NOUNS]) == 0:
                    noun_candidates = [nc for nc in self[self.WORDS] 
                                       if match("^[^a-zäöü]", nc) 
                                       is not None]
                    for word in noun_candidates:
                        if word in ref_nouns \
                        or match("^[A-Z]{2,}", word) is not None:
                            self[self.NOUNS].append(word.strip())
                    self.write_file(self.NOUNS)
            else:
                self[self.NOUNS] = clean_iterable(n)
                
            return self[self.NOUNS]
               
        if trans[0] == True:
            self._translate_words(en_to_de_dict=trans[1])
        
        return self[self.WORDS]

    def get_stems(self, uniq=False, trans=(False, None), relev=False):
        """
        @param uniq: Defaults to False, i. e. returns not-unique stems.
                     Can be changed by providing True. Optional 
                     setting.
        @param trans: First argument specifies if translation should
                      occur; second argument gives possibility to 
                      specify a bi-dictionary as object.
        @param relev: Only return relevant stems, of the sort useful
                      for classification, i. e. w/o stop words or very
                      rare words (appearing e. g. only once everywhere).
        @return: Set of stems found upon the words. Create once.
        """
        var = self.STEMS
        if uniq == True:
            var = self.STEMS_UNIQ
            self[var] = set(self[var]) # Ugly: This shouldn't be necessary
        
        if len(self[var]) == 0:
            for word in self.get_words(trans=trans):
                # Below argument "german" for compatibility reasons 
                # w/ older versions of NTLK
                if uniq == True:
                    # Code breaks here under some circumstances, w/o
                    # above ugly line.
                    self[var].add(Stemmer("german").stem(word))
                    pass
                else:
                    self[var].append(Stemmer("german").stem(word))
                    pass
            self.write_file(self.STEMS)
            
        if relev == True:
            idf_file = get_stems_file(measure="_idf")
            
            
            idf_dict = DictFromFile(idf_file)
            self[var] = get_classification_stems(self[var], idf_dict)
            
        return self[var]
    
    """
    WORDS_BY_EDIT_DISTANCE = "words_by_edit_distance"
    TOP_WORDS = "top_words"
    TEXT_FREQ_DIST = "text_freq_dist"
    """
    
    ###################################################################
    # Other getters, not relying on data in an instance of this class
    ###################################################################
    
    def get_filesize(self):
        """
        @return: Return integer with file size of the xml document
        """
        return getsize(self.get_xml_filename())
    
    def get_rawlen(self): 
        """
        @return: Returns raw content as string, which originally 
                 was found in <content> node
        """
        return len(self.get_rawcontent())
    
    def get_file(self, key, hashsum=True):
        """
        @param key: Specifies which data to look at, e. g. "NOUNS" 
                   (str).
        @param hashsum: If True (default) return not only file's 
                        contents, but also hashsum, otherwise return 
                        only file content.
        @return: Hashsum (str) of this document's data in some context
                 specified by param key. If no file available returns 
                 None values.
        """
        sha512sum = None
        content = None
        
        folder = self._get_folder_by_key(key)
        try:
            f = open(folder + self[self.DOC_ID], "r", get_def_enc())
            content = f.readlines()
            sha512sum = sha512("".join(content). \
                                encode(get_def_enc())).hexdigest()
            f.close()
        except IOError:
            pass
        
        if hashsum == False:
            return content
        # Otherwise: Return a tuple
        return content, sha512sum
    
    def _get_folder_by_key(self, key):
        """
        Internal method to return the right folder to store linguistic
        material.
        
        @param key: Key indicating which folder we want, e. g. "NOUNS"
        @return: str being folder path, based on the key value passed.
        
        """
        folder = ""
        if key == self.WORDS:
            folder = get_wordsdir()
        elif key == self.NOUNS:
            folder = get_wordsdir(pos='n')
        elif key == self.STEMS:
            folder = get_stemsdir()
        # More folder variations to add
        return folder
    
    ##########################################
    # Methods to print content to the terminal
    ##########################################
    
    def print_rawcontent(self): 
        """
        Print the <content> part of the message to the terminal. 
        """        
        print self[self.CONTENT_TAG]
        
    ########################
    # Methods to write files
    ########################
    
    def write_file(self, key, hashsum=True):
        """
        Writes a file (name: document name) to a specified folder.
        @param key: Specifies which data to write, based on the 
                    key of the data stored in in this object, 
                    e. g. "WORDS" or "NOUNS".
        @param hashsum: Defaults to True and is used to write an 
                        hashsum of the file to an hashfile.
        """
        folder = self._get_folder_by_key(key)
        
        doc_id = self[self.DOC_ID]
        doc_as_str = "\n".join(self[key]).encode(get_def_enc())
        sha512sum = ""
        if (hashsum == True):
            hashdict = HashDict() 
            sha512sum = sha512(doc_as_str).hexdigest()
            hashdict[folder + doc_id] = sha512sum
            hashdict.save()
        
        if not exists(folder): 
            print "Folder " + folder + " doesn't exist."
            try:
                makedirs(folder)
                print "Folder " + folder + " created."
            except Exception, e:
                print str(e)
        
        f = open(folder + doc_id, "w", get_def_enc())
        f.write(doc_as_str)
        f.close()

    def write_content(self, content_format="line", content_type="raw"):
        """
        Write files in different possible formats and content types to 
        a folder on disk.
        @param content_format: If "line" writes content unit line per 
                             line.
        @param content_type: If "raw", write tokens as is; other values
                            like "words" may (become) possible.
        """
        d = get_mailfolder(content_format=content_format)
        if not exists(d):
            print "Folder " + d + " not availabe. Create it."
            makedirs(d)

        # For now only "raw" content_type exists, and "line" 
        # content_format
        f = open(d + self[self.DOC_ID], "w", get_def_enc())       
        for t in self.get_tokens():
            f.write(t + "\n")
        f.close()
        
    ##############
    # Misc methods
    ##############
    def _load_hashsums(self):
        """
        Simply read in the hashsumsfile (again) and save it here.
        This is important when changes occurred during processing.
        """
        self[self.HASHSUMS] = HashDict()
        
    def _translate_words(self, en_to_de_dict=None):
        """
        Translate words using (for now) an en-de-bidix.
        @param en_to_de_dict: A dictionary object can be directly
                              passed, to increase speed when
                              translating several documents'
                              words.
        """
        if (en_to_de_dict == None):
            en_to_de_dict = EnToDeDict()
        
        # Substitute all (English) words by (potential) German ones
        for i in range(len(self[self.WORDS])):
            try: 
                self[self.WORDS][i] = en_to_de_dict[self[self.WORDS][i]]
            except KeyError:
                pass