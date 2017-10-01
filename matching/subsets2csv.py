import sys
import re
import json
import random

def retrieve_arxiv_id (art):
    has_closest = "closest_arxiv" in art
    has_arxiv = "arxiv" in art

    if has_closest and has_arxiv:
        raise Exception ("Error! Both matched and unmatched!\n"+art)
    if not has_closest and not has_arxiv:
        raise Exception ("Error! Neither matched nor unmatched!\n"+art)

    if has_closest:
        return art["closest_arxiv"][0]
    elif has_arxiv:
        return art["arxiv"][0]
    else:
        raise Exception ("Statement should not be reached")

def main ():
    articles = []
    for fname in sys.argv[1:]:
        with open(fname) as f:
            articles.extend (json.load (f))

    random.shuffle (articles)

    for art in articles:
        arxiv_id = retrieve_arxiv_id (art)
        if arxiv_id is None:
                raise Exception("Cannot find arxiv id:\n"+str(art))
        if art["dblp"] is None:
                raise Exception("Cannot find dblp id:\n"+str(art))

        dblp_id = art["dblp"]
        arxiv_url = "http://arxiv.org/abs/" + arxiv_id
        dblp_url = "http://dblp.org/rec/html/" + dblp_id

        print "%s,%s," % (arxiv_url, dblp_url)


if __name__ == '__main__':
    main()
