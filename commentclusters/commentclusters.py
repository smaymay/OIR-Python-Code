from __future__ import print_function
import argparse
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import pandas as pd
import json

# commentclusters.py
# written for the OIR at Wellesley College
# 2016-06-08
# code adapted from original written by 
#         Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck <L.J.Buitinck@uva.nl>
#         Chyi-Kwei Yau <chyikwei.yau@gmail.com>

__author__ = "M. Svanberg"

"""
=======================================================================================
Topic extraction with Non-negative Matrix Factorization and Latent Dirichlet Allocation
=======================================================================================

Given an excel file, with a specified column name which's rows are comments, 
creates a json file containing the lists of top words in the cluster.

Example command line:
    $ python commentclusters.py 2016_WELLESLEY_CATCHALLCOMMENTS.xlsx catchall 35 10

"""

# Original Author's comment:
# Load the dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

def extractData(data_samples):

    print("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, #max_features=n_features,
                                    stop_words='english')
    t0 = time()
    tfidf = tfidf_vectorizer.fit_transform(data_samples)
    print("done in %0.3fs." % (time() - t0))
    
    print("Fitting the NMF model with tf-idf features,"
        "n_samples=%d and n_features=%d..."
        % (n_samples, n_features))
    t0 = time()
    nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)
    print("done in %0.3fs." % (time() - t0))

    print("Preparing output file")
    t0 = time()
    
    tf_feature_names = tfidf_vectorizer.get_feature_names()
    
    output = {'topics': []}
    for topic_idx, topic in enumerate(nmf.components_):
        output['topics'].append(list(([tf_feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]])))
                        
    print("done in %0.3fs." % (time() - t0))
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('filename', type=str, help="name of excel file holding the comments")
    parser.add_argument('colname', type=str, help="name of column holding the comments")
    parser.add_argument('n_topics', type=int, help="number of clusters")
    parser.add_argument('n_top_words', type=int, help="number of top words per cluster")
    
    args = parser.parse_args()
    
    n_samples = 2000
    n_features = 1000
    n_topics = args.n_topics
    n_top_words = args.n_top_words
    
    
    print("Loading dataset...")
    t0 = time()
    comments = pd.read_excel(args.filename).fillna('missing')
    com_list = comments[args.colname].apply(lambda x: x.encode('utf-8')).tolist()
    print("done in %0.3fs." % (time() - t0))
    
    dictionary = extractData(com_list)
    
    with open ('comclust-' + args.filename.split('.')[0] + '-' 
            + str(args.n_topics) + '-' 
            + str(args.n_top_words) + '.json', 'w') as outFile:
        outFile.write(json.dumps(dictionary,
                             sort_keys=True,
                             indent=2, separators=(',', ':')))
