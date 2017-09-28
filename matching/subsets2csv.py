import sys
import re
import json

CONVERT_DBLP_RE = re.compile (r'(.*)/[^/]*\.html#(.*)')

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

def convert_dblp (dblp_str):
    # example: db/conf/icml/icml2017.html#SilverHHSGHDRRB17
    # -->      conf/icml/SilverHHSGHDRRB17
    sys.stderr.write (str(dblp_str)+"\n")
    m = CONVERT_DBLP_RE.match(dblp_str)
    if not m:
        raise Exception("Could not match string "+str)
    return m.group(1) + m.group(2)

def main ():
    for fname in sys.argv[1:]:

        with open(fname) as f:
            articles = json.load (f)

        for art in articles:
            arxiv_id = retrieve_arxiv_id (art)
            if arxiv_id is None:
                raise Exception("Cannot find arxiv id:\n"+str(art))
            if art["url"] is None:
                raise Exception("Cannot find dblp id:\n"+str(art))

            dblp_id = art["dblp"]
            arxiv_url = "http://arxiv.org/abs/" + arxiv_id
            dblp_url = "http://dblp.org/rec/html/" + dblp_id

            print "%s,%s," % (arxiv_url, dblp_url)


if __name__ == '__main__':
    main()
