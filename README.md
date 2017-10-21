# Popularity of arXiv.org within Computer Science

This directory generates all of the results from the paper 

  Charles Sutton and Gong. Popularity of arXiv.org within Computer Science.
  Arxiv Pre-print 1710.05225. 2017.
  https://arxiv.org/abs/1710.05225
  http://groups.inf.ed.ac.uk/cup/csarxiv/

The main results are generated ina series of three Jupyter notebooks. Executing them all in sequence will download the latest version of the data
and regenerate all of the results. The notebooks call a set of scripts, which are in the subdirectories.

 * [0. Download and Preprocess Data.ipynb](https://github.com/casutton/cs-arxiv-popularity-code/blob/master/0.%20Download%20and%20Preprocess%20Data.ipynb)
 is a bash notebook that runs scripts to download the xml data dump from DBLP and the relevant arXiv data from its API. The scripts that the notebooks calls
 are in the `arxiv/` and `dblp/` subdirectories. The downloaded data is written to the `generated/dblp` and `generated/arxiv/` directories.
 * [1. Record Linkage between DBLP and Arxiv.ipynb](https://github.com/casutton/cs-arxiv-popularity-code/blob/master/1.%20Record%20Linkage%20between%20DBLP%20and%20Arxiv.ipynb)
 is a bash notebook that runs scripts to perform the approximate record linakage between DBLP and arXiv, as described in the paper. This notebook calls scripts
 in the `matching/` subdirectory.The downloaded data is written to the `generated/matching` directories.
 * [2. Explore and Validate Data.ipynb](https://github.com/casutton/cs-arxiv-popularity-code/blob/master/2.%20Explore%20and%20Validate%20Data.ipynb) shows some exploratory data analysis
 that we did for data cleaning. The main result here is a graph for every conference in the study, the total number of published papers per year,
 and the total number of papers per year that was matched to arXiv.
 * [3. Preprint Percentage Analysis.ipynb](https://github.com/casutton/cs-arxiv-popularity-code/blob/master/3.%20Preprint%20Percentage%20Analysis.ipynb) actually generates all
 of the figures from the paper. These are written to the `figures/` directory.
 
To summarize what all the subdirectories are:

* `arxiv/`: Scripts for downloading arxiv data. You don't need to call these directly, you can run notebook 0 instead.
* `dblp/`: Scripts for downloading DBLP data. You don't need to call these directly, you can run notebook 0 instead.
* `matching/`: Code for record linkage of arxiv-->DBLP. You don't need to call these directly, you can run notebook 1 instead.
* `data/`: This contains data that was manually generated:
   * `data/deadlines.csv`: Submission, notification, and conference dates for all conferences that were included in the study of whether arXiv e-prints were
   submitted during the review process. Hopefully the headers in the CSV are self explanatory. These were collected manually from the conference web sites.
   * `data/manually_labeled_coref.csv`: Contains a sample of 50 papers that the matching heuristic selected as (DBLP, arXiv) match, manually labelled
   as to whether they were really coreferent. Details of how these papers were sampled are described in the paper. The column `t_match` is whether the annotator
   believed that the titles were the same, `a_match` whether the authors were the same, and `p_match` whether the papers as a whole were the same
* `figures/`: Figures used in the paper. Everything in this directory is automatically generated. The version of the directory that is committed
to the repo are the figures that are used in the current version of the paper.
* `generated/`: Citation data used in the paper. Everything in this directory is automatically generated. The version of the directory that is committed
to the repo are the figures that are used in the current version of the paper.
* `iclr2017/`: This directory contains a manually-saved dump of the OpenReview page for the ICLR 2017 conference. This is just to document the statement that we made in the intorduction about the number of submissions to ICLR 2017.

# Where to Start

* If you want to download all of the most recent papers and regenerate the entire analysis, run each of the Jupyter notebooks fully in numerical order.
* If you want to explore the precise version of the data that we used in the paper, then fully execute [3. Preprint Percentage Analysis.ipynb](https://github.com/casutton/cs-arxiv-popularity-code/blob/master/3.%20Preprint%20Percentage%20Analysis.ipynb),
which will load all of the data from the `generated` directory, and add your analysis at the end. It's OK to execute notebook 2 if you want, but do not execute the other notebooks, as these will blow away the data in the `generated/` directory.
