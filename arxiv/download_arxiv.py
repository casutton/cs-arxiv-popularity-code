# Downloads metadata of all articles in CS since 1993 from Arxiv.
# This will take about an hour.
# Outputs saved as XML files in generated/raw folder

import urllib
import time
import contextlib
import xml.etree.ElementTree as ElementTree

# yes, this is global. sorry!
n = 0

def parse_resumption_token (xmlstring):
    token = ""
    root = ElementTree.XML(xmlstring)
    for el in root.iter():
        el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
        if el.tag == ('resumptionToken'):
            token = el.text
            break
    return token
                
def download_arxiv_pubs(set):
    global n
    
    url = "http://export.arxiv.org/oai2?verb=ListRecords&from=1999-01-01&set=%s&metadataPrefix=arXivRaw" % set
    data = urllib.urlopen(url).read()

    with open('generated/arxiv/raw/data%s.xml' % n, 'w') as out_file:
        out_file.write(data)

    token = parse_resumption_token (data)
    n = n + 1

    while token:
        print n
        time.sleep(10)

        url2 = "http://export.arxiv.org/oai2?verb=ListRecords&resumptionToken=%s" % token
        with contextlib.closing(urllib.urlopen(url2)) as input:
            data = input.read()

        with open('generated/arxiv/raw/data'+ str(n) + '.xml', 'w') as out_file:
            out_file.write(data)

        token = parse_resumption_token (data)
            
        n = n + 1
        
    time.sleep (10)

    
def main():
    # download both cs and stat (download stat because of stat.ML)
    download_arxiv_pubs ('cs')
    download_arxiv_pubs ('stat')

    
if ( __name__ == "__main__"):
    main()

