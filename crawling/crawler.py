#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
from cupang_crawler import CupangCrawler

if __name__ == "__main__":

    crawler = CupangCrawler()

    # setting search keyword
    crawler.init('LG전자 디오스 매직스페이스 양문형 냉장고 ')

    # store search urls
    crawler.search_item_list()

    # get reviews for urls
    crawler.item_list_load()

    count = 1
    while not crawler.list_done:
        crawler.search_item()
        count = count + 1

    crawler.end()
