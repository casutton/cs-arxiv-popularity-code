# -*- coding: utf-8 -*-
__author__ = 'Kay'

import sys
import xml.sax
import re
import codecs
import json
import glob
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import re

import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../matching'))
import match_cnf_arxiv

STOP_WORDS = set(stopwords.words('english'))
STOP_WORDS.update(['.', ',', '"', "'", '?', '!', ':', ';', '-', '(', ')', '[', ']', '{', '}'])


class EntryHandler(xml.sax.ContentHandler):

    def __init__(self, paper_list):
        self.paper_list = paper_list
        self.CurrentData = ""
        self.title = ""
        self.author = ""
        self.id = ""
        self.category = ""
        self.submit = ""
        self.flag = 0

    # start event
    def startElement(self, tag, attributes):
        self.CurrentData = tag

        if tag == "metadata":
            pass

        elif tag == "version" and attributes["version"] == "v1":
            self.flag = 1
            
        elif tag == "date":
            pass
            
        else:
            self.flag = 0

    # end event
    def endElement(self, tag):
        if tag == "metadata":
            date = self.submit.split(' ')
            self.submit = date[1]+'-'+date[2]+'-'+date[3]
            
            alldata = {'title': self.title, 'authors': self.author, 'category': self.category, 'submit': self.submit, 'id': self.id, 'year':int(date[3]) }
            self.paper_list.append (alldata)
            
            self.title = ""
            self.author = ""
            self.submit = ""
            self.id = ""
            self.category = ""
            self.CurrentData = ""
            self.flag = 0

        elif tag == "title":
            self.title = re.sub('\n +', ' ', self.title)

        elif tag == "authors":
            self.author = re.sub('\n +', ' ', self.author)

        elif tag == "categories":
            pass


    # content event
    def characters(self, content):
        if self.CurrentData == "date" and self.flag == 1:
            self.submit = self.submit + content
        elif self.CurrentData == "title":
            self.title = self.title + content
        elif self.CurrentData == "authors":
            self.author = self.author + content
        elif self.CurrentData == "id":
            self.id = self.id + content        
        elif self.CurrentData == "categories":
            self.category = content


def tokenize_arxiv_entry (item):
    # title = item['title'].lower()
    # titlelist = [i for i in wordpunct_tokenize(title) if i not in STOP_WORDS]
    # authors = re.sub(r'\(\w+((-|\s|,|/|&|\'|\.|\"|;)*\w*|\(\w+|\s|\d+\)*)*\)', '', item['authors']).lower()
    # authorlist =  wordpunct_tokenize(authors)
    # surnames = []
    # for i in range(len(authorlist)):
    #     if (i == len(authorlist)-1) or (authorlist[i+1] == ",") or (authorlist[i+1] == "and"):
    #         if (authorlist[i] != ",") and (authorlist[i] != "and"):
    #             surnames.append(authorlist[i])
    # item['bow_title'] = titlelist
    # item['bow_authors'] = surnames
    item['bow_title'] = match_cnf_arxiv.bowify_title (item['title'])
    item['bow_authors'] = match_cnf_arxiv.bowify_authors (item['authors'])
    return


def read_all_files():
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # rewrite contentHandler
    paper_list = []
    Handler = EntryHandler(paper_list)
    parser.setContentHandler( Handler )

    all_files = glob.glob ('generated/arxiv/raw/data*.xml')
    for fname in all_files:
        parser.parse(fname)

    print "Processing %d papers from arxiv" % len(paper_list)
    
    n = 0
    for paper in paper_list:
        tokenize_arxiv_entry (paper)
        n += 1
        if (n % 1000) == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
            
    with codecs.open('generated/arxiv/json/arxiv_articles.json', 'w', 'utf-8') as out_file:
        json.dump (paper_list, out_file, indent=2)



if ( __name__ == "__main__"):
    read_all_files()

