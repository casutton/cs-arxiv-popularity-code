from csrankings import csv2dict_str_str, startyear, endyear, areadict, confdict, arealist, venues, pagecount, startpage, ElementTree, pageCountThreshold, countPaper, conf2confdict
import json
import config
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import re
import codecs
import gzip

import sys
import os

I = 0
MAX = 1

def parseDBLP():
    authlogs = {}
    interestingauthors = {}
    authorscores = {}
    authorscoresAdjusted = {}
    coauthors = {}
    papersWritten = {}
    allpapers = []
    counter = 0

    with gzip.open('generated/dblp/dblp.xml.gz', mode='r') as f:
    # with open('generated/foo/foo.xml', mode='r') as f:

        oldnode = None

        for (event, node) in ElementTree.iterparse(f, events=['start', 'end']):
            if (oldnode is not None):
                oldnode.clear()
            oldnode = node

            foundArticle = False
            authorsOnPaper = 0
            authorName = ""
            confname = ""
            year = -1
            pageCount = -1
            startPage = -1
            number = 0
            volume = 0
            paperinfo = dict()
            paperinfo['authors'] = list()

            if (node.tag == 'inproceedings' or node.tag == 'article'):

                paperinfo["dblp"] = node.get("key")

                # First, check if this is one of the conferences we are looking for.

                for child in node:
                    if (child.tag == 'booktitle' or child.tag == 'journal'):
                        confname = child.text
                        if (confname in confdict):
                            areaname = confdict[confname]
                            paperinfo['area'] = areaname
                            foundArticle = True
                        if (confname in conf2confdict):
                            paperinfo['venue'] = conf2confdict[confname]
                        else:
                            paperinfo['venue'] = confname
                    if (child.tag == 'volume'):
                        volume = child.text
                    if (child.tag == 'number'):
                        number = child.text
                    if (child.tag == 'title'):
                        # this way instead of child.text as the latter breaks if the title contains HTML
                        # this way strips all XML/HTML tags from within the title
                        paperinfo['title'] = ElementTree.tostring(child, method="text", encoding="utf-8").strip(" \n\t.")
                        paperinfo['title'] = paperinfo['title'].decode('latin1')
                    if child.tag == 'year':
                        if child.text is not None:
                            year = int(child.text)
                            paperinfo['year'] = year
                    if child.tag == 'pages':
                        pageCount = pagecount(child.text)
                        startPage = startpage(child.text)
                    if child.tag == 'url':
                        # sometimes this is None, even when there is clearly
                        #  a URL in the xml file. I cannot replicate this on a small
                        #  example, so I have no idea what is going on
                        paperinfo["url"] = child.text
                    if child.tag == 'author':
                        authorName = child.text
                        if authorName is not None:
                            authorName = unicode(authorName).strip()
                            paperinfo['authors'].append(authorName)
                            authorsOnPaper += 1

                # One of our conferences?
                if not foundArticle:
                    continue

                # One of the papers we count?
                if not countPaper(confname, year, volume, number, startPage, pageCount):
                    continue

                # sanity check for errors where no title shows up
                #  (detects any recurrences of a bug where titles weren't included if contained XML
                if not paperinfo.get('title', False):
                    print ElementTree.dump (node)
                    print paperinfo
                    raise Exception("No title")

                # If we get here, we have a winner.

                for child in node:
                    if child.tag == 'author':
                        authorName = child.text
                        authorName = authorName.strip()
                        if True:
                            # print "here we go",authorName, confname, authorsOnPaper, year
                            logstring = authorName.encode('utf-8') + " ; " + confname + " " + str(year)
                            tmplist = authlogs.get(authorName, [])
                            tmplist.append(logstring)
                            authlogs[authorName] = tmplist
                            interestingauthors[authorName] = interestingauthors.get(authorName, 0) + 1
                            authorscores[(authorName, areaname, year)] = authorscores.get((authorName, areaname, year), 0) + 1.0
                            authorscoresAdjusted[(authorName, areaname, year)] = authorscoresAdjusted.get((authorName, areaname, year), 0) + 1.0 / authorsOnPaper

                # record all paper info for logging
                allpapers.append(paperinfo)

    return (allpapers, interestingauthors, authorscores, authorscoresAdjusted, authlogs)

STOP_WORDS = set(stopwords.words('english'))
STOP_WORDS.update(['.', ',', '"', "'", '?', '!', ':', ';', '-', '(', ')', '[', ']', '{', '}'])


(allpapers, intauthors_gl, authscores_gl, authscoresAdjusted_gl, authlog_gl) = parseDBLP()

## This is not needed for the prepublication study, but leaving it in so
## that the data can be eyeballed as a sanity check
f = open('generated/dblp/generated-author-info.csv','w')
f.write('"name","area","count","adjustedcount","year"\n')
for (authorName, area, year) in authscores_gl:
    count = authscores_gl[(authorName, area, year)]
    countAdjusted = authscoresAdjusted_gl[(authorName, area, year)]
    f.write(authorName.encode('utf-8'))
    f.write(',')
    f.write(area)
    f.write(',')
    f.write(str(count))
    f.write(',')
    f.write(str(countAdjusted))
    f.write(',')
    f.write(str(year))
    f.write('\n')
f.close()

print len(allpapers)

f = codecs.open('generated/dblp/all-papers.json','w', 'utf-8')
# f = codecs.open('generated/foo/all-papers.json','w', 'utf-8')
data = json.dumps (allpapers, indent=2, ensure_ascii=False)
f.write(unicode(data))
f.close ()
