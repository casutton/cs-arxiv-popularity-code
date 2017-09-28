import json
import argparse
import random
import match_cnf_arxiv
import sys

YEAR_INDEX = dict()

def build_indices (arxiv):
    for art in arxiv:
        year = int(art['year'])
        lst = YEAR_INDEX.get(year, [])
        lst.append (art)
        YEAR_INDEX[year] = lst

# Jaccard similarity on bow_title and bow_authors
def compute_jaccard (art_dblp, art_arxiv):

    # recompute bow version of title and authors if not already cached
    if 'bow_title' not in art_dblp: art_dblp['bow_title'] = match_cnf_arxiv.bowify_title (art_dblp['title'])
    if 'bow_title' not in art_arxiv: art_arxiv['bow_title'] = bmatch_cnf_arxiv.owify_title (art_arxiv['title'])
    if 'bow_authors' not in art_dblp: art_dblp['bow_authors'] = match_cnf_arxiv.bowify_authors (art_dblp['authors'])
    if 'bow_authors' not in art_arxiv: art_arxiv['bow_authors'] = match_cnf_arxiv.bowify_authors (art_arxiv['authors'])

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

    return (t_sim, a_sim)

def closest_arxiv (art_dblp):
    list_to_check = YEAR_INDEX [art_dblp["year"]]

    best_avg_sim = 0
    best_match = None
    best_t_sim = 0
    best_a_sim = 0

    for art_arxiv in list_to_check:
        (t_sim, a_sim) = compute_jaccard(art_dblp, art_arxiv)
        avg_sim = (t_sim + a_sim) / 2.0
        if avg_sim > best_avg_sim:
            best_avg_sim = avg_sim
            best_match = art_arxiv
            best_t_sim = t_sim
            best_a_sim = a_sim

    return (best_match, best_t_sim, best_a_sim)


def main ():
    parser = argparse.ArgumentParser(description='Match DBLP articles to arxiv.')
    parser.add_argument('--dblp-file', action="store",
                    help='JSON file with dump from matching algoirthm')
    parser.add_argument('--arxiv-file', action="store",
                    help='JSON file with dump from arxiv')
    parser.add_argument('--N', default=25, action="store", type=int,
                    help='Number to sample')
    parser.add_argument('--seed', default=0, action="store", type=int,
                    help='Random seed')
    parser.add_argument('--threshold', default=0.5, action="store", type=float,
                    help='Only sample non-matches with this threshold')
    parser.add_argument('--prefix', default='', action="store",
                    help='prefix for output files')

    args = parser.parse_args()

    with open(args.dblp_file) as f:
        articles = json.load (f)
    with open(args.arxiv_file) as f:
        arxiv = json.load (f)
    random.seed(args.seed)

    build_indices(arxiv)

    matched = []
    non_matched = []
    n_nomatch = 0
    for a in articles:
        if 'arxiv' in a:
            matched.append (a)
        else:
            non_matched.append (a)

    ## Generating close sample is more complex. What we're trying to do
    ##  is draw args.N random DBLP articles, but only from the set
    ##  of DBLP articles who are at least args.threshold away from an
    ##  arxiv article

    ## First, we'll split all of the non-matched DBLP articles into
    ##  those that are close or far from their nearest arxiv article

    all_close = []
    all_far = []

    nart = 0
    for art in non_matched:
        (arxiv_art, title_dist, author_dist) = closest_arxiv (art)
        art['author_dist'] = author_dist
        art['title_dist'] = title_dist

        if arxiv_art is not None:
            art['closest_arxiv'] = list(arxiv_art["id"])
        else:
            art['closest_arxiv'] = None

        if author_dist > args.threshold and title_dist > args.threshold:
            all_close.append(art)
        else:
            all_far.append(art)

        nart += 1
        if nart % 500 == 0:
            print ".",
            sys.stdout.flush()

    ## Print statistics

    print "Total DBLP articles = %d" % len(articles)
    print "Total matched articles = %d" % len(matched)
    print "Total close articles = %d" % len(all_close)
    print "Total non-close articles = %d" % len(all_far)

    ## Now generate the samples

    matched_sample = random.sample (matched, args.N)
    close_sample = random.sample(all_close, args.N)

    ## And write to disk

    matched_file = args.prefix + "_matched.json"
    with open (matched_file, 'w') as f:
            json.dump (matched_sample, f, indent=2)

    close_file = args.prefix + "_close.json"
    with open (close_file, 'w') as f:
            json.dump (close_sample, f, indent=2)




if __name__ == '__main__':
    main()
