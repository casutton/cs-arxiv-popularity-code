# Edit this file to determine what papers will be included

# Minimum page count to be included (default: 6)
pageCountThreshold = 6

# Consider pubs in this date range only (default: 1970-2269).
startyear = 2007
endyear   = 2017

# If true, only output papers that contain an author in faculty-affiliations.csv (default: True)
checkAffiliation = False

# List of venues that should be counted, along with a mapping to research areas
areadict = {
    #
    # Max three most selective venues per area for now.
    #
    # SIGPLAN
    'plan' : ['POPL', 'PLDI'], # , 'OOPSLA'],
    # SIGHPC
    'hpc' : ['SC', 'HPDC', 'ICS'],
    # SIGLOG
    'log' : ['CAV', 'CAV (1)', 'CAV (2)', 'LICS', 'CSL-LICS'],
    # SIGSOFT
    'soft' : ['ICSE', 'ICSE (1)', 'ICSE (2)', 'SIGSOFT FSE', 'ESEC/SIGSOFT FSE', 'ASE'],
    # SIGOPS
    # - OSDI/SOSP alternate years, so are treated as one venue; USENIX ATC has two variants in DBLP
    'ops' : ['SOSP', 'OSDI', 'EuroSys', 'USENIX Annual Technical Conference', 'USENIX Annual Technical Conference, General Track'],
    # SIGARCH
    'arch' : ['ISCA', 'MICRO', 'ASPLOS'],
    # SIGACT
    'act' : ['STOC', 'FOCS','SODA'],
    # SIGCOMM
    'comm' : ['SIGCOMM', 'INFOCOM', 'NSDI'],
    # SIGSAC
    # - USENIX Security listed twice to reflect variants in DBLP
    'sec' : ['IEEE Symposium on Security and Privacy', 'ACM Conference on Computer and Communications Security', 'USENIX Security Symposium', 'USENIX Security'],
    'mlmining' : ['NIPS', 'ICML','KDD','ICML (1)','ICML (2)','ICML (3)'],
    'ai' : ['AAAI', 'AAAI/IAAI', 'IJCAI'],
    # AAAI listed to account for AAAI/IAAI joint conference
    'mod' : ['VLDB', 'PVLDB', 'SIGMOD Conference'],
    # SIGGRAPH
    # - special handling of TOG to select SIGGRAPH and SIGGRAPH Asia
    'graph' : ['ACM Trans. Graph.', 'SIGGRAPH'],
    # SIGMETRICS
    # - Two variants for each, as in DBLP.
    'metrics' : ['SIGMETRICS','SIGMETRICS/Performance','IMC','Internet Measurement Conference'],
    # SIGIR
    'ir' : ['WWW', 'SIGIR'],
    # SIGCHI
    'chi' : ['CHI','UbiComp','Ubicomp','UIST'],
    'nlp' : ['EMNLP','ACL','ACL (1)', 'ACL (2)', 'NAACL', 'HLT-NAACL',
        'ACL/IJCNLP', #-- in 2009 was joint
        'COLING-ACL', #-- in 1998 was joint
        'EMNLP-CoNLL',#-- in 2012 was joint
        'HLT/EMNLP',  #-- in 2005 was joint
    ],
    'vision' : ['CVPR', 'CVPR (1)', 'CVPR (2)', 'ICCV', 'ECCV (1)', 'ECCV (2)', 'ECCV (3)', 'ECCV (4)', 'ECCV (5)', 'ECCV (6)', 'ECCV (7)'],
    # SIGMOBILE
    'mobile' : ['MobiSys','MobiCom','MOBICOM','SenSys'],
    'robotics' : ['ICRA','ICRA (1)', 'ICRA (2)', 'IROS','Robotics: Science and Systems'],
    'crypt' : ['CRYPTO', 'CRYPTO (1)', 'CRYPTO (2)', 'CRYPTO (3)', 'EUROCRYPT', 'EUROCRYPT (1)', 'EUROCRYPT (2)', 'EUROCRYPT (3)'],
    # SIGBio
    # - special handling for ISMB proceedings in Bioinformatics special issues.
    'bio' : ['RECOMB', 'ISMB', 'Bioinformatics', 'Bioinformatics [ISMB/ECCB]', 'ISMB/ECCB (Supplement of Bioinformatics)'],
    # SIGDA
    'da' : ['ICCAD', 'DAC'],
    # SIGBED
    'bed' : ['RTSS', 'RTAS', 'EMSOFT', 'IEEE Real-Time and Embedded Technology and Applications Symposium'],
    # special handling of IEEE TVCG to select IEEE Vis and VR proceedings
    'vis' : ['IEEE Visualization', 'VR', 'IEEE Trans. Vis. Comput. Graph.']
}

# Mapping of research areas to readable names
labeldict = {
    'plan' : "Programming languages",
    'hpc' :  "High performance computing",
    'log' : "Logic and verification",
    'soft' : "Software engineering",
    'ops' : "Operating systems",
    'arch' : "Computer architectures",
    'act' : "Algorithms and complexity",
    'comm' : "Networking",
    'sec' : "Security",
    'mlmining' : "ML & DM",
    'ml' : "Machine learning",
    'mining' : "Data mining",
    'ai' : "Artificial intelligence",
    'mod' : "Databases",
    'graph' : "Graphics",
    'metrics' : "Measurement",
    'ir' : "Information retrieval",
    'chi' : "HCI",
    'nlp' : "NLP",
    'vision' : "Vision",
    'mobile' : "Mobile computing",
    'robotics' : "Robotics",
    'crypt' : "Cryptography",
    'bio' : "Bioinformatics",
    'da' : "Design automation",
    'bed' : "Embedding systems",
    'vis' : "Visualization",
}

# DBLP distinguishes multiple volumes, colocated conferences and so on, that we do not want to distinguish in the graphs
conf2confdict = {
    'CAV (1)': 'CAV',
    'CAV (2)': 'CAV',
    'ICSE (1)': 'ICSE',
    'ICSE (2)': 'ICSE',
    'ESEC/SIGSOFT FSE': 'FSE',
    'SIGSOFT FSE': 'FSE',
    'SOSP': 'SOSP/OSDI',
    'OSDI': 'SOSP/OSDI',
    'USENIX Annual Technical Conference': 'USENIX',
    'USENIX Annual Technical Conference, General Track': 'USENIX',
    'USENIX Security Symposium': 'USENIX Security',
    'AAAI/IAAI' : 'AAAI',
    'SIGMETRICS/Performance': 'SIGMETRICS',
    'Internet Measurement Conference':  'IMC',
    'Ubicomp' : 'UbiComp',
    'ACL (1)': 'ACL',
    'ACL (2)': 'ACL',
    'ACL/IJCNLP': 'ACL',
    'COLING-ACL': 'ACL',
    'EMNLP-CoNLL': 'EMNLP',
    'HLT/EMNLP': 'EMNLP',
    'CVPR (1)': 'CVPR',
    'CVPR (2)': 'CVPR',
    'ECCV (1)': 'ECCV',
    'ECCV (2)': 'ECCV',
    'ECCV (3)': 'ECCV',
    'ECCV (4)': 'ECCV',
    'ECCV (5)': 'ECCV',
    'ECCV (6)': 'ECCV',
    'ECCV (7)': 'ECCV',
    'MOBICOM': 'MobiCom',
    'ICRA (1)': 'ICRA',
    'ICRA (2)': 'ICRA',
    'Robotics: Science and Systems': 'RSS',
    'CRYPTO (1)': 'CRYPTO',
    'CRYPTO (2)': 'CRYPTO',
    'CRYPTO (3)': 'CRYPTO',
    'EUROCRYPT (1)': 'EUROCRYPT',
    'EUROCRYPT (2)': 'EUROCRYPT',
    'EUROCRYPT (3)': 'EUROCRYPT',
    'ISMB/ECCB (Supplement of Bioinformatics)': 'ISMB',
    'IEEE Visualization': 'IEEE Vis',
    'IEEE Symposium on Security and Privacy': 'IEEE S&P',
    'SIGMOD Conference': 'SIGMOD',
    'ACM Conference on Computer and Communications Security': 'CCS',
    # treat PVLDB and VLDB as same conference (after 2007 this becomes PVLDB)
    'VLDB': 'PVLDB',
    'CSL-LICS': 'LICS',
    'IEEE Real-Time and Embedded Technology and Applications Symposium': 'RTAS',
    'Bioinformatics [ISMB/ECCB]': 'ISMB',
    'ICML (1)': 'ICML',
    'ICML (2)': 'ICML',
    'ICML (3)': 'ICML',
    # Several conferences appear only as special issues in journals.
    # The CSRankings code is careful to pick up ONLY those journal issues
    #  which are actually conference proceedings. Therefore, whenever we
    #  see the relevant journal title, we will rename to the conference.
    # Also, we don't try to distinguish SIGGRAPH vs SIGGRAPH Asia
    # or IEEE VIS versus VR because it would require logic to choose
    # the venue name based on the issue number of the journal.
    # This doesn't seem worth the trouble.
    "Bioinformatics": "ISMB",
    "IEEE Trans. Vis. Comput. Graph.": "IEEE VIS + VR",
    "VR": "IEEE VIS + VR",
    "ACM Trans. Graph.": "SIGGRAPH (+Asia)"
}
