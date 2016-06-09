from __future__ import print_function
from time import time
import pandas as pd
import argparse
import json
import math

# catvalues.py
# written for the OIR at Wellesley College
# 2016-06-09

__author__ = "M. Svanberg"

"""
=======================================================================================
Evalution of how relevant a cluster is to a comment
=======================================================================================

Given an excel file with with 
a specified column name which's rows are comments, 
a json file containing the lists of top words in clusters in ranked orders,
adds a value for the relationship between cluster and comment, for every cluster
and comment.

Example command line input:
    $ python catvalues.py 2016_WELLESLEY_CATCHALLCOMMENTS.xlsx catchall comclust-2016_WELLESLEY_CATCHALLCOMMENTS-35-10.json

"""

def weighCategory(text):
    weight = 0
    words = text.split()
    for word in words:
        try:
            weight += clusters[cat][word.lower()]
        except KeyError:
            pass
    return int((weight)/float(math.sqrt(len(words))) > args.threshold)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('filename', type=str, help="name of excel file holding the comments")
    parser.add_argument('colname', type=str, help="name of column holding the comments")
    parser.add_argument('jsonfile', type=str, help="name of json file")
    parser.add_argument('threshold', type=float, help="cutoff for what is a category")
    
    args = parser.parse_args()

    print("Loading dataset...")
    t0 = time()
    comments = pd.read_excel(args.filename).fillna('missing')
    comments[args.colname] = comments[args.colname].apply(lambda x: x.encode('utf-8'))
    print ("done in " + str(time()-t0) + "s.")
    
    print("Loading clusters...")
    t0 = time()

    with open(args.jsonfile) as json_file:
        clusters = json.load(json_file)
    
    print('Number of clusters: ' + str(len(clusters)))
    print("done in %0.3fs." % (time() - t0))
    
    print("Calculating and inserting cat values...")
    t0 = time()
    for cat in clusters.keys():
        comments[cat] = comments[args.colname].apply(weighCategory)
    print("done in %0.3fs." % (time() - t0))


    comments.to_csv(args.filename.split('.')[0] + "_%0.3f.csv" % args.threshold)