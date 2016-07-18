import pandas as pd
import argparse
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from time import time

# sentiment.py
# written for the OIR at Wellesley College
# 2016-06-13

__author__ = "M. Svanberg"

"""
================================================================================
            Sentiment analysis
================================================================================
Given an excel file, holding comments and their categories, creates a json file
containing the sentiment analysis of the comments per category. 

Example command line:
    $ python sentiments.py 2016_WELLESLEY_CATCHALLCOMMENTS.xlsx catchall

"""

def findSentimentOfCat(cat):
    
    catList = data[data[cat] == True][args.colname].tolist()
    feelings = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}
    
    for comment in catList:
        try:
            ss = sid.polarity_scores(comment)
            for k in sorted(ss):
                feelings[k] += ss[k]
        except AttributeError:
            pass
            
    for k in feelings:
        try:
            feelings[k] = feelings[k]/len(catList)
        except ZeroDivisionError:
            pass
    
    sentiment[cat] = feelings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('xslxname', type=str, help="name of excel file holding the categorized comments")
    parser.add_argument('colname', type=str, help="name of column holding the comments")
    args = parser.parse_args()
    
    print("Loading dataset...")
    t0 = time()
    data = pd.read_excel(args.xslxname)
    cats = list(data.columns.values)[2:]
    print("done in %0.3fs." % (time() - t0))
    
    sentiment = {}
    sid = SentimentIntensityAnalyzer()
    
    print("Extracting feelings...")
    t0 = time()
    for cat in cats:
        findSentimentOfCat(cat)
    print("done in %0.3fs." % (time() - t0))
    
    print("Creating json...")
    t0 = time()
    
    with open ('sentiment-' + args.xslxname.split('.')[0] + 
            '.json', 'w') as outFile:
        outFile.write(json.dumps(sentiment,
                             sort_keys=True,
                             indent=2, separators=(',', ':')))
                             
    print("done in %0.3fs." % (time() - t0))