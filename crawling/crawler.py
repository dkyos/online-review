#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
from cupang_crawler import CupangCrawler

if __name__ == "__main__":

    crawler = CupangCrawler()

    # setting search keyword
    #crawler.init('삼성전자 초순도 청정 큐브 공기청정기 가정용')
    crawler.init('삼성전자 초순도 청정 큐브 공기청정기 가정용 AX80N9080WWD 80㎡')

    # store search urls
    crawler.search_item_list()

    # get reviews for urls
    crawler.item_list_load()

    count = 1
    while not crawler.list_done:
        crawler.search_item()
        count = count + 1

    crawler.end()
