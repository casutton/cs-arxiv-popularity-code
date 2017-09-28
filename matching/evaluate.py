import match_cnf_arxiv
import glob
import os.path
import json

TEST_DIRECTORY = "../test_data/"

def load_test_data(dir = TEST_DIRECTORY):
    data = []
    files = glob.glob (os.path.join (TEST_DIRECTORY, "*.json"))
    for fname in files:
        with open(fname) as f:
            data.extend (json.load (f))
    return data
    
def average_performance (data, matcher):
    TP, FP, FN, TN = 0, 0, 0, 0
    
    for pair in data:
        art1 = { "title": pair['title1'], "authors": pair['authors1']  }
        art2 = { "title": pair['title2'], "authors": pair['authors2']  }
        was_predicted_match = matcher(art1, art2)

        if was_predicted_match:
            if 'matched' in pair:
                TP += 1
            else:
                FP += 1
        else:
            if 'matched' in pair:
                FN += 1
            else:
                TN += 1
        
    Precision = float(TP)/(TP+FP) if (TP + FP) > 0 else 0.0
    Recall = float(TP)/(TP+FN) if (TP + FN) > 0 else 0.0

    return {'P': Precision, 'R': Recall,  "TP": TP, "FP": FP, "FN": FN, "TN": TN }


if __name__ == '__main__':
        data = load_test_data()
        results = average_performance(data, match_cnf_arxiv.titlematch)
        print results
        print "Exact title match precision = %.4f" % results['P']
        print "Exact title match recall = %.4f" % results['R']

        results = average_performance(data, match_cnf_arxiv.bowmatch)
        print results
        print "BOW match precision = %.4f" % results['P']
        print "BOW match recall = %.4f" % results['R']

        results = average_performance(data, match_cnf_arxiv.bowmatch2)
        print results
        print "BOW2 match precision = %.4f" % results['P']
        print "BOW2 match recall = %.4f" % results['R']
