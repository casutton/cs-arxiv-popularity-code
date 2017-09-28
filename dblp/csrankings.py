# from lxml import etree as ElementTree
import xml.etree.ElementTree as ElementTree
import htmlentitydefs
import csv
import operator
import re

from config import *

# import gzip

# parser = ElementTree.XMLParser(attribute_defaults=True, load_dtd=True)
parser = ElementTree.XMLParser()

# Match ordinary page numbers (as in 10-17).
pageCounterNormal = re.compile('(\d+)-(\d+)')
# Match page number in the form volume:page (as in 12:140-12:150).
pageCounterColon = re.compile('[0-9]+:([1-9][0-9]*)-[0-9]+:([1-9][0-9]*)')

def startpage(input):
    if (input is None):
        return 0
    pageCounterMatcher1 = pageCounterNormal.match(input)
    pageCounterMatcher2 = pageCounterColon.match(input)
    start = 0

    if (not (pageCounterMatcher1 is None)):
        start = int(pageCounterMatcher1.group(1))
    else:
        if (not (pageCounterMatcher2 is None)):
            start = int(pageCounterMatcher2.group(1))
    return start


def pagecount(input):
    if (input is None):
        return 0
    pageCounterMatcher1 = pageCounterNormal.match(input)
    pageCounterMatcher2 = pageCounterColon.match(input)
    start = 0
    end = 0
    count = 0

    if (not (pageCounterMatcher1 is None)):
        start = int(pageCounterMatcher1.group(1))
        end   = int(pageCounterMatcher1.group(2))
        count = end-start+1
    else:
        if (not (pageCounterMatcher2 is None)):
            start = int(pageCounterMatcher2.group(1))
            end   = int(pageCounterMatcher2.group(2))
            count = end-start+1
    return count



# ISMB proceedings are published as special issues of Bioinformatics.
# Here is the list.
ISMB_Bioinformatics = { 2017: (33, 14), # source: https://academic.oup.com/bioinformatics/article-lookup/doi/10.1093/bioinformatics/btx321
                        2016 : (32, 12),
                        2015 : (31, 12),
                        2014 : (30, 12),
                        2013 : (29, 13),
                        2012 : (28, 12),
                        2011 : (27, 13),
                        2010 : (26, 12),
                        2009 : (25, 12),
                        2008 : (24, 13),
                        2007 : (23, 13)
}

# TOG special handling to count only SIGGRAPH proceedings.
TOG_SIGGRAPH_Volume = { 2017 : (36, 4), # source: https://dl.acm.org/citation.cfm?id=3072959&CFID=813068326&CFTOKEN=22710666
                        2016 : (35, 4),
                        2015 : (34, 4),
                        2014 : (33, 4),
                        2013 : (32, 4),
                        2012 : (31, 4),
                        2011 : (30, 4),
                        2010 : (29, 4),
                        2009 : (28, 3),
                        2008 : (27, 3),
                        2007 : (26, 3),
                        2006 : (25, 3),
                        2005 : (24, 3),
                        2004 : (23, 3),
}

# TOG special handling to count only SIGGRAPH Asia proceedings.
TOG_SIGGRAPH_Asia_Volume = { 2016 : (35, 6),
                             2015 : (34, 6),
                             2014 : (33, 6),
                             2013 : (32, 6),
                             2012 : (31, 6),
                             2011 : (30, 6),
                             2010 : (29, 6),
                             2009 : (28, 5),
                             2008 : (27, 5)
}

# TVCG special handling to count only IEEE Visualization
TVCG_Vis_Volume = { 2017 : (23, 1),
                    2016 : (22, 1),
                    2014 : (20, 12),
                    2013 : (19, 12),
                    2012 : (18, 12),
                    2011 : (17, 12),
                    2010 : (16, 6),
                    2009 : (15, 6),
                    2008 : (14, 6),
                    2007 : (13, 6),
                    2006 : (12, 5)
}

# TVCG special handling to count only IEEE VR
TVCG_VR_Volume = { 2017: (23, 4), # Source: http://ieeexplore.ieee.org/document/7878159/
                   2016: (22, 4),
                   2015: (21, 4),
                   2014: (20, 4),
                   2013: (19, 4),
                   2012: (18, 4) }

# ICSE special handling to omit short papers.
# Contributed by Zhendong Su, UC Davis.
# Short papers start at this page number for these proceedings of ICSE (and are thus omitted,
# as the acceptance criteria differ).
ICSE_ShortPaperStart = { 2013 : 851,
                         2012 : 957,
                         2011 : 620,
                         2010 : 544,
                         2009 : 550,
                         2007 : 510,
                         2006 : 411,
                         2005 : 478,
                         2003 : 477,
                         2002 : 534,
                         2001 : 502,
                         2000 : 518,
                         1999 : 582,
                         1998 : 419,
                         1997 : 535 }

# ASE accepts short papers and long papers. Long papers appear to be at least 10 pages long,
# while short papers are shorter.
ASE_LongPaperThreshold = 10

# Build a dictionary mapping conferences to areas.
# e.g., confdict['CVPR'] = 'vision'.
confdict = {}
venues = []
for k, v in areadict.items():
    for item in v:
        confdict[item] = k
        venues.append(item)

# The list of all areas.
arealist = areadict.keys();

def csv2dict_str_str(fname):
    with open(fname, mode='r') as infile:
        reader = csv.reader(infile)
        #for rows in reader:
        #    print rows[0], "-->", rows[1]
        d = {unicode(rows[0].strip(),'utf-8'): unicode(rows[1].strip(),'utf-8') for rows in reader}
    return d

def sortdictionary(d):
    return sorted(d.iteritems(), key=operator.itemgetter(1), reverse = True)

# Acceptance criteria: true iff we will count this paper.
def countPaper(confname, year, volume, number, startPage, pageCount):
    if year < startyear or year > endyear:
        return False

    # Special handling for ISMB.
    if (confname == 'Bioinformatics'):
        if ISMB_Bioinformatics.has_key(year):
            (vol, num) = ISMB_Bioinformatics[year]
            if (volume != str(vol)) or (number != str(num)):
                return False
        else:
            return False

    # Special handling for ICSE.
    if ((confname == 'ICSE') or (confname == 'ICSE (1)') or (confname == 'ICSE (2)')):
        if ICSE_ShortPaperStart.has_key(year):
            pageno = ICSE_ShortPaperStart[year]
            if startPage >= pageno:
                # Omit papers that start at or beyond this page,
                # since they are "short papers" (regardless of their length).
                return False

    # Special handling for SIGGRAPH and SIGGRAPH Asia.
    if (confname == 'ACM Trans. Graph.'):
        SIGGRAPH_Conf = False
        if TOG_SIGGRAPH_Volume.has_key(year):
            (vol, num) = TOG_SIGGRAPH_Volume[year]
            if (volume == str(vol)) and (number == str(num)):
                SIGGRAPH_Conf = True
        if TOG_SIGGRAPH_Asia_Volume.has_key(year):
            (vol, num) = TOG_SIGGRAPH_Asia_Volume[year]
            if (volume == str(vol)) and (number == str(num)):
                SIGGRAPH_Conf = True
        if not SIGGRAPH_Conf:
            return False

    # Special handling for IEEE Vis and VR
    if (confname == 'IEEE Trans. Vis. Comput. Graph.'):
        Vis_Conf = False
        if TVCG_Vis_Volume.has_key(year):
            (vol, num) = TVCG_Vis_Volume[year]
            if (volume == str(vol)) and (number == str(num)):
                Vis_Conf = True
        if TVCG_VR_Volume.has_key(year):
            (vol, num) = TVCG_VR_Volume[year]
            if (volume == str(vol)) and (number == str(num)):
                Vis_Conf = True
        if not Vis_Conf:
            return False

    # Special handling for ASE.
    if (confname == 'ASE'):
        if pageCount < ASE_LongPaperThreshold:
            # Omit short papers (which may be demos, etc.).
            return False

    # SPECIAL CASE FOR conferences that have incorrect entries (as of 6/22/2016).
    # Only skip papers with a very small paper count,
    # but above 1. Why?
    # DBLP has real papers with incorrect page counts
    # - usually a truncated single page. -1 means no
    # pages found at all => some problem with journal
    # entries in DBLP.
    tooFewPages = False
    if ((pageCount != -1) and (pageCount < pageCountThreshold)):
        tooFewPages = True
        exceptionConference = confname == 'SC'
        exceptionConference |= confname == 'SIGSOFT FSE' and year == 2012
        exceptionConference |= confname == 'ACM Trans. Graph.' and int(volume) >= 26 and int(volume) <= 36
        if exceptionConference:
            tooFewPages = False
    if tooFewPages:
        return False

    return True
