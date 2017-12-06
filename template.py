#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
from dk_header import *
from dk_logger import dk_logger
from dk_csv import *

# singleton logger
logger = dk_logger.get_logger()

def analyze(filename):
    """Run test."""
    logger.info("start analyzing...")
    df = load_csv_to_df(filename)
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'filename',
        help='The filename of testing you\'d like to analyze.')
    args = parser.parse_args()

    analyze(args.filename)
