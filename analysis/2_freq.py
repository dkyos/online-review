#!/usr/bin/env python
#-*- coding: utf-8 -*-

import csv
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from konlpy.tag import Kkma, Hannanum, Komoran, Mecab, Twitter

mecab = Mecab()

import argparse
from dk_header import *
from dk_logger import dk_logger
from dk_csv import *

# singleton logger
logger = dk_logger.get_logger()

def str2datetime(s):
    return datetime.strptime(s,  '%Y.%m.%d' )

def load(filename):
    """Run test."""
    logger.info("start analyzing...")
    df = load_csv_to_df(filename)
    return df

def cleaning(comments):
    #doc = mecab.nouns(comments)
    #doc = " ".join(i for i in doc)
    #return doc
    return comments

def ready_text(df):
    df = df.astype(str)
    df = df.replace('nan','')
    df = df[df['review_content'].apply(lambda x: len(x)>5) ]
    #print(len(df[df.review_content == np.nan]))
    #print(len(df[df.review_content == "nan"]))
    #print(len(df[df.review_content == ""]))

    text = df.applymap(cleaning)['review_content']
    return text

def dk_freq(text_list):
    #vect = CountVectorizer().fit(text_list)
    vect = CountVectorizer(min_df=1, ngram_range=(3,3)).fit(text_list)
    X = vect.transform(text_list)
    
    df = pd.DataFrame({'term': vect.get_feature_names()
        , 'occurrences':np.asarray(X.sum(axis=0)).ravel().tolist()})
    
    #df['frequency'] = df['occurrences']/np.sum(df['occurrences'])
    word_freq_df = df[df['occurrences'] >= 2]
    
    print (word_freq_df.sort_values('occurrences',ascending = False).head(10))

    return word_freq_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'filename',
        help='The filename of testing you\'d like to analyze.')
    args = parser.parse_args()

    df = load(args.filename)
    logger.info("read_csv[%s]: %s" % (args.filename, df.shape))

    grouped = df.groupby('product_info')
    for product_info, group in grouped:
        if group.shape[0] > 100:
            print("="*30)
            logger.info(product_info)
            text_list = ready_text(group)
            #print(text_list)
            dk_freq(text_list)



