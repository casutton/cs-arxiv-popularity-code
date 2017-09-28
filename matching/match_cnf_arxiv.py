import json
import sys
import argparse
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import re

DBLP_PAPER_FILE = "../dblp/generated/all-papers.json"
ARXIV_PAPER_FILE = "../arxiv/generated/json/arxiv_articles.json"

BOW_MAX_THRESHOLD = 1.0 - 1e-10
BOW_MIN_THRESHOLD = 0.4 - 1e-10

STOP_WORDS = set(stopwords.words('english'))
STOP_WORDS.update(['.', ',', '"', "'", '?', '!', ':', ';', '-', '(', ')', '[', ']', '{', '}'])



def build_indices (arxiv):
    yridx = dict()
    for art in arxiv:
        year = int(art['year'])
        lst = yridx.get(year, [])
        lst.append (art)
        yridx[year] = lst

    titidx = dict()
    for art in arxiv:
        title = art['title'].lower()
        lst = titidx.get(title, [])
        lst.append (art)
        titidx[title] = lst

    allidx = dict()
    allidx['year'] = yridx
    allidx['title'] = titidx

    return allidx


### CANOPY FUNCTIONS

def yearcanopy (art_dblp, index_arxiv):
    year = art_dblp['year']
    retlist = []
    yridx = index_arxiv['year']
    retlist.extend(yridx.get(year, []))
    retlist.extend(yridx.get(year-1, []))
    return retlist

def titlecanopyexact (art_dblp, index_arxiv):
    dblp_title = art_dblp['title'].lower()
    retlist = index_arxiv['title'].get(dblp_title, [])
    return retlist

### MATCHERS

def titlematch (art_dblp, art_arxiv):
    try:
        title0 = art_dblp['title'].lower()
        title1 = art_arxiv['title'].lower()
        return title0 == title1
    except:
        print art_dblp
        print art_arxiv
        raise
    return False

def titleauthormatch (art_dblp, art_arxiv):
    try:
        title0 = art_dblp['title'].lower()
        title1 = art_arxiv['title'].lower()

        if (title0 != title1): return False

        author_count = bow_author_unnormalized(art_dblp, art_arxiv)

        return author_count > 0
    except:
        print art_dblp
        print art_arxiv
        raise
    return False


# This function is copied pasted from preprocessing scripts in dblp/ and arxiv/
#   that's because we precompute this when preprocessing each data set
#   copied here to allow running the match computation without the preprocessing
def bowify_title (title):
    titlelist = [i for i in wordpunct_tokenize(title.lower ()) if i not in STOP_WORDS]
    return titlelist

# remove parenthesized things from author names
def deparenify (string):
    if '(' in string:
        string = re.sub(r'(\([^)]*\))', '', string)
    return string

def bowify_authors (authors):
    if isinstance (authors, list):
        auth_noparen = [ deparenify(a.lower()) for a in authors ]
    elif isinstance (authors, str) or isinstance (authors, unicode):
        # remove parenthesized things from author names
        authors = deparenify(authors.lower())
        # split individiual authors in string via , and "and"
        auth_noparen = re.split (r'\s*(?:,(?: and)?|(?: and))\s*', authors)

    names = [ re.split(r'\.?\s*', a) for a in auth_noparen ]
    names = [ [ a for a in name if (a != "") ] for name in names ]

    return names

# Jaccard similarity on bow_title and bow_authors
def bowmatch (art_dblp, art_arxiv):

    # recompute bow version of title and authors if not already cached
    if 'bow_title' not in art_dblp: art_dblp['bow_title'] = bowify_title (art_dblp['title'])
    if 'bow_title' not in art_arxiv: art_arxiv['bow_title'] = bowify_title (art_arxiv['title'])
    if 'bow_authors' not in art_dblp: art_dblp['bow_authors'] = bowify_authors (art_dblp['authors'])
    if 'bow_authors' not in art_arxiv: art_arxiv['bow_authors'] = bowify_authors (art_arxiv['authors'])

    title1 = art_dblp['bow_title']
    title2 = art_arxiv['bow_title']
    count = 0
    for word in title1:
        if word in title2:
            count += 1
    t_sim = float(count)/(len(title1)+len(title2)-count)

    authors1 = [ a[-1] if len(a) > 0 else [] for a in art_dblp['bow_authors'] ]
    authors2 = [ a[-1] if len(a) > 0 else [] for a in art_arxiv['bow_authors'] ]
    count = 0
    for word in authors1:
        if word in authors2:
            count += 1
    a_sim = float(count)/(len(authors1)+len(authors2)-count)

    matched = max(t_sim,a_sim) > BOW_MAX_THRESHOLD and min(t_sim, a_sim) > BOW_MIN_THRESHOLD

    return matched


# Jaccard similarity on bow_title and bow_authors
def bowmatch2 (art_dblp, art_arxiv):

    # recompute bow version of title and authors if not already cached
    if 'bow_title' not in art_dblp: art_dblp['bow_title'] = bowify_title (art_dblp['title'])
    if 'bow_title' not in art_arxiv: art_arxiv['bow_title'] = bowify_title (art_arxiv['title'])
    if 'bow_authors' not in art_dblp: art_dblp['bow_authors'] = bowify_authors (art_dblp['authors'])
    if 'bow_authors' not in art_arxiv: art_arxiv['bow_authors'] = bowify_authors (art_arxiv['authors'])

    title1 = art_dblp['bow_title']
    title2 = art_arxiv['bow_title']
    count = 0
    for word in title1:
        if word in title2:
            count += 1
    t_sim = float(count)/(len(title1)+len(title2)-count)

    authors1 = [ a for lst in art_dblp['bow_authors'] for a in lst ]
    authors2 = [ a for lst in art_arxiv['bow_authors'] for a in lst ]
    count = 0
    for word in authors1:
        if word in authors2:
            count += 1
    a_sim = float(count)/(len(authors1)+len(authors2)-count)

    matched = max(t_sim,a_sim) > BOW_MAX_THRESHOLD and min(t_sim, a_sim) > BOW_MIN_THRESHOLD

    return matched


# Jaccard similarity on bow_title and bow_authors
def bow_author_unnormalized (art_dblp, art_arxiv):

    # recompute bow version of title and authors if not already cached
    if 'bow_authors' not in art_dblp: art_dblp['bow_authors'] = bowify_authors (art_dblp['authors'])
    if 'bow_authors' not in art_arxiv: art_arxiv['bow_authors'] = bowify_authors (art_arxiv['authors'])

    authors1 = [ a[-1] if len(a) > 0 else [] for a in art_dblp['bow_authors'] ]
    authors2 = [ a[-1] if len(a) > 0 else [] for a in art_arxiv['bow_authors'] ]
    count = 0
    for word in authors1:
        if word in authors2:
            count += 1

    return count


### FINDER

def findmatch (art, index_arxiv, matcher, canopy):
    matches = []
    to_check = canopy (art, index_arxiv)
    for art_arxiv in to_check:
        if matcher (art, art_arxiv):
            id = art_arxiv['id']  # intentionally throw exception if id missing
            if not id in matches:
                matches.append (id)
    return matches

def main ():
    parser = argparse.ArgumentParser(description='Match DBLP articles to arxiv.')
    parser.add_argument('--dblp-file', default=DBLP_PAPER_FILE, action="store",
                    help='JSON file with dump from dblp')
    parser.add_argument('--arxiv-file', default=ARXIV_PAPER_FILE, action="store",
                    help='JSON file with dump from arxiv')
    parser.add_argument('--output-file', default='output.json', action="store",
                    help='Directory to save output json file in')
    parser.add_argument('--matcher', default='titleauthormatch', action="store",
                    help='matching function to use between papers')
    parser.add_argument('--canopy', default='titlecanopyexact', action="store",
                    help='canopy function to use to look up arxiv candidates')
    parser.add_argument('-N', default=sys.maxsize, type=int, action="store", help="stop after this many papers")

    args = parser.parse_args()

    with open(args.dblp_file) as f:
        dblp = json.load (f)
    with open(args.arxiv_file) as f:
        arxiv = json.load (f)

    index_arxiv = build_indices (arxiv)
    nmatch = 0
    nart = 0

    for art in dblp:
        nart += 1
        matches = findmatch (art, index_arxiv, globals()[args.matcher], globals()[args.canopy])
        if matches:
            art['arxiv'] = matches
            nmatch += 1
        if nart % 1000 == 0:
            print ".",
            sys.stdout.flush()
        if nart > args.N:
            break
    print

    print "Total articles matched = ", nmatch
    print "Total articles checked = ", nart

    with open (args.output_file, 'w') as f:
        json.dump (dblp, f, indent=2)



if __name__ == '__main__':
    main()
