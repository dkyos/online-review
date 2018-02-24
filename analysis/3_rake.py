#!/usr/bin/env python
#-*- coding: utf-8 -*-

import csv
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from konlpy.tag import Kkma, Hannanum, Komoran, Mecab, Twitter
from collections import defaultdict
import nltk
from rake_nltk import Rake
import argparse
from dk_header import *
from dk_logger import dk_logger
from dk_csv import *

mecab = Mecab()
rg = Rake(language='korean')
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
    print(text)
    return text

def do_rake(text_list):
    text = str(text_list)
    rg.extract_keywords_from_text(text)
    print("---------------")
    print(rg.get_ranked_phrases())


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
        if group.shape[0] > 30:
            print("="*30)
            logger.info(product_info)
            text_list = ready_text(group)
            do_rake(text_list)



