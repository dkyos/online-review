#!/usr/bin/env python
#-*- coding: utf-8 -*-

import csv
import pandas as pd
import numpy as np
from matplotlib import rcParams
import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx
from datetime import datetime
from PIL import Image
from os import path
import matplotlib.patches as mpatches
import random

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

def modify_cols(df):
    df = df.astype(str)
    df['timestamp'] = df['date'].apply( str2datetime ) 
    df['year_days'] = df['timestamp'].apply(lambda x : (x-datetime(x.year,1,1)).days)
    #df['days'] = df['timestamp'].apply(lambda x : (x-datetime(2012,1,1)).days)
    df['year'] = df['timestamp'].apply(lambda x : (x.year))
    df['month'] = df['timestamp'].apply(lambda x : (x.month))

    df = df.sort_values('timestamp').reset_index(drop=True)
    return df

def daily_stat(df):
    daily_stats = df.groupby('date').agg({'review_content':len}).describe()
    logger.info(u'하루에 평균 %.1f 건' % (daily_stats.loc['mean']))
    logger.info(u'하루에 최대 %d 건' % (daily_stats.loc['max']))
    logger.info(u'평균 %.1f단어 %d글자로 씀' % 
        ( df['review_content'].apply(lambda x: len(x.split(' '))).mean(),
        df['review_content'].apply(lambda x: len(x)).mean()) )

    logger.info(df.groupby('year')['review_content'].count())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'filename',
        help='The filename of testing you\'d like to analyze.')
    args = parser.parse_args()

    df = load(args.filename)
    df = modify_cols(df)
    daily_stat(df)



