#-*- coding: utf-8 -*-
import csv
# import psycopg2
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
import logging
from bs4 import BeautifulSoup as Soup
from selenium.common.exceptions import NoSuchElementException
import pickle
import json
import sys 
import itertools
from bs4 import BeautifulSoup
import re
import time
import os
import os.path
import datetime
import pandas as pd
import numpy as np
import validators

OUTPUT_DIR = './prod_list/';
MARKET_NAME = 'cupang';
CUPANG_URL = 'https://www.coupang.com';
SEARCH_INPUT_CSS = 'input[class="coupang-search ad-keyword is-speech"]';
NEXT_BTN_CSS = 'a[class="btn-next"]';

tag_to_find = "a";
attr_to_get = "href";

LOG_FILE = './log.txt';
logger = logging.getLogger('mylogger');

class CupangCrawler:

    def __init__(self):

        # debug info warning error critical
        logger.setLevel(logging.INFO)
        fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

        fileHandler = logging.FileHandler(LOG_FILE)
        logger.addHandler(fileHandler)
        fileHandler.setFormatter(fomatter)

        #streamHandler = logger.StreamHandler()
        #logger.addHandler(streamHandler)
        #streamHandler.setFormatter(fomatter)

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.current_url = None
        self.keyword = None
        self.item_list_nm = None
        self.crawl_data_nm = None
        self.item_lists = None
        self.item_lists_num = 0
        self.list_done = False
        logger.info("Creating crawler is done.")

    def openPage(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(3)
            self.current_url = url
        except:
            logger.error("driver get excepttion")
        return  

    def init(self, keyword):

        self.keyword = keyword;
        self.item_list_nm = OUTPUT_DIR + MARKET_NAME + '_' \
            + self.keyword + "_list.txt"
        self.crawl_data_nm = OUTPUT_DIR + MARKET_NAME + '_' \
            + self.keyword + "_data.txt"

        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chromeOptions.add_experimental_option("prefs",prefs)

        self.driver = webdriver.Chrome(
            executable_path='/usr/bin/chromedriver'
            , chrome_options=chromeOptions)

        #self.driver = webdriver.PhantomJS()

        self.openPage(CUPANG_URL);

        logger.info("Initialize complete.")

    def end(self):
        self.driver.quit()
        logger.info("Done !!!!")

    def search_item_list(self):

        if not os.path.exists(self.item_list_nm):
            open(self.item_list_nm, 'a').close()

        if not os.path.exists(self.crawl_data_nm):
            open(self.crawl_data_nm, 'a').close()

        # Send search keyword to web
        search = self.driver.find_element_by_css_selector(SEARCH_INPUT_CSS)
        search.send_keys(self.keyword)
        search.send_keys(Keys.RETURN)
        time.sleep(1.5)

        list_set = set()

        # count = 0
        # screenshot_name = 'fb_%s.png' % count
        # self.driver.save_screenshot(screenshot_name)
        # count = count + 1

        current_page = 1;
        num = 1
        while True:
        
            bsObj = BeautifulSoup(self.driver.page_source, "html5lib")

            for link in bsObj.find_all(tag_to_find, href=re.compile("^(/vp/products?)")):

                if attr_to_get in link.attrs:
                    link_url = CUPANG_URL + link.attrs[attr_to_get]
                if not validators.url(link_url):
                    continue

                if "data-product-id" in link.attrs:
                    prod_id = link.attrs["data-product-id"]
                if "data-item-id" in link.attrs:
                    item_id = link.attrs["data-item-id"]
                if "data-vendor-item-id" in link.attrs:
                    vendor_item_id = link.attrs["data-vendor-item-id"]

                if prod_id in list_set:
                    logger.info("[%s] product is already added" % prod_id)
                else:
                    logger.info("[%s] product add" % prod_id)
                    list_set.add(prod_id)
                    parsed_item_list = [num, prod_id, item_id, vendor_item_id, link_url]
                    logger.info(parsed_item_list)
                    # add Item to list 
                    self.item_list_update(parsed_item_list)
                    num = num + 1;

            try:
                next_page = self.driver.find_element_by_css_selector(NEXT_BTN_CSS);
            except NoSuchElementException:
                logger.debug("last page done")
                break;
    
            current_page = current_page + 1;
            venue = wait(self.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, NEXT_BTN_CSS)))
            #venue.click()
            self.driver.execute_script('arguments[0].click()', venue)
            time.sleep(1)
        
    def item_list_update(self, parsed_item_list):
        with open(self.item_list_nm, "a", encoding='utf-8') as f:
            w = csv.writer(f, delimiter = '|', quotechar = ',' )
            w.writerow(parsed_item_list)
        return 

    # Item List Loading for crawling
    def item_list_load(self):

        def item_list_gen(filename):
            if os.path.exists(filename):
                with open(filename, "r", encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter='|')
                    for row in reader:
                        yield row[0:5]
            else:
                logger.error("There is no file to load. (%s)" % self.item_list_nm)
            return

        self.item_list_nm = self.item_list_nm.encode('utf-8')
        self.item_lists = item_list_gen(self.item_list_nm)

        review_data = ["0", "review_count", "total_review", "product_id", "item_id", "vendor_item_id"
                    , "product_info", "date", "rating", "member_id", "review_id", "review_content"]
        logger.info(review_data)
        self.review_update(review_data)

        return

    def search_item(self):      # [prod_id, item_id, vendor_item_id, link_url]
        try:
            if self.item_lists is not None:
                item_list = next(self.item_lists)
            else:
                logger.debug("There is no item lists to crawl.")
                return

            logger.info(item_list)
            # item_list = [num, prod_id, item_id, vendor_item_id, link_url]
            self.get_reviews(item_list);

            # Clear Cookies on the browser => todo
            #if self.item_lists_num > 10:
            logger.info("Start: deleteAllCookies")
            self.driver.delete_all_cookies()
            logger.info("End: deleteAllCookies")

        except StopIteration:
            logger.info("StopIteration")
            self.list_done = True
            #self.driver.quit()
            return
        except:
            logger.error("Unexpected error:", sys.exc_info()[0])
            time.sleep(0.5)
            return

    def review_update(self, review_data):
        with open(self.crawl_data_nm, "a", encoding='utf-8') as f:
            w = csv.writer(f, delimiter = '|', quotechar = ',' )
            w.writerow(review_data)
        return 


    # item_list = [num, prod_id, item_id, vendor_item_id, link_url]
    def get_reviews(self, item_list):
        num             = item_list[0]
        prod_id         = item_list[1]
        item_id         = item_list[2]
        vendor_item_id  = item_list[3]
        url             = item_list[4]

        self.item_lists_num = self.item_lists_num + 1;
        logger.info(str(self.item_lists_num) + ': ' +  url)

        self.openPage(url)

        logger.info('wait clickable for review button')
        venue = wait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, 
            '//*[@id="product-contents-placeholder"]/div/div/div[2]/div[1]/div[1]/div/div/a[2]'
        )))
        logger.info('click review button')
        #venue.click()
        self.driver.execute_script('arguments[0].click()', venue)

        try:
            logger.info('wait element present sdp-review__article__search-result')
            element_present = EC.presence_of_element_located((By.XPATH, 
                '//*[@id="prod-review"]/div/div[5]/section[3]'
            ))
            wait(self.driver, 3).until(element_present)
            logger.info('element found sdp-review__article__search-result')
        except TimeoutException as ex:
            logger.info('TimeoutException');
            logger.info(ex)
        except NoSuchElementException as ex:
            logger.info('NoSuchElementException')
            logger.info(ex)

        # wait to find the total review count
        try:
            logger.info('wait element sdp-review__average__total-star__info-count')
            element_present = EC.presence_of_element_located((By.XPATH, 
                '//*[@id="prod-review"]/div/div[3]/section[1]/div[1]/div[2]'
            ))
            wait(self.driver, 3).until(element_present)
            logger.info('element found sdp-review__average__total-star__info-count')
        except TimeoutException as ex:
            logger.info('TimeoutException');
            logger.info(ex)
        except NoSuchElementException as ex:
            logger.info('NoSuchElementException')
            logger.info(ex)

        soup = Soup(self.driver.page_source, "html5lib")
        total_review = 0
        select_data = soup.select_one(
            'div.sdp-review__average__total-star__info-count')
        if select_data != None:
            total_review = int(select_data.text.replace(',',''))
        logger.info("Total Review = [%d] " % total_review)

        page_num     = 1;
        current_num  = 2;
        review_count = 0;

        while True:

            #self.driver.save_screenshot("2_review.png")
            soup = Soup(self.driver.page_source, "html5lib")

            #<article class="sdp-review__article__list js_reviewArticleReviewList">
            for review in soup.select('article.sdp-review__article__list.js_reviewArticleReviewList'):

                # initialize
                product_info = rating = Date = None;
                member_id = User = review_id = review_content = None

                review_count = review_count + 1;
                logger.info("========================")
                logger.info("count = [%d]" % (review_count));

                select_data = review.select_one(
                    'div.sdp-review__article__list__info__product-info__name')
                if select_data != None:
                    logger.info("Product info = [%s] " % select_data.text)
                    product_info = select_data.text

                select_data = review.select_one(
                    'div.sdp-review__article__list__info__product-info__star-orange.js_reviewArticleRatingValue')
                if select_data != None:
                    logger.info("rating = [%d]" % int(select_data['data-rating']) )
                    rating = int(select_data['data-rating'])
       
                select_data = review.select_one(
                    'div.sdp-review__article__list__info__product-info__reg-date')
                if select_data != None:
                    logger.info("Date = [%s] " % select_data.text)
                    Date = select_data.text
       
                select_data = review.select_one(
                    'span.sdp-review__article__list__info__user__name.js_reviewUserProfileImage')
                if select_data != None:
                    logger.info("data-member-id = [%d]" % int(select_data['data-member-id']) )
                    member_id = int(select_data['data-member-id'])
                    logger.info("User = [%s] " % select_data.text)
                    User = select_data.text

                select_data = review.select_one(
                    'div.sdp-review__article__list__help.js_reviewArticleHelpfulContainer')
                if select_data != None:
                    logger.info("data-review-id = [%d]" % int(select_data['data-review-id']) )
                    review_id = int(select_data['data-review-id']) 

                select_data = review.select_one(
                    'div.sdp-review__article__list__review__content')
                if select_data != None:
                    select_data = select_data.text
                    select_data = select_data.strip()
                    select_data = select_data.rstrip()
                    select_data = select_data.replace('\n', '').replace('\r', '')
                    logger.info("Review = [%s] " % select_data)
                    review_content = select_data

                review_data = [num, review_count, total_review, prod_id, item_id, vendor_item_id
                    , product_info, Date, rating, member_id, review_id, review_content]
                logger.info(review_data)
                self.review_update(review_data)

            #self.driver.save_screenshot("2_review.png")
            current_num = current_num + 1;
            page_num    = page_num + 1;

            # 12 is next_page button
            if current_num == 13:
                # 2 already readed by next page button
                # we start from 3
                current_num = 3;

            try:
                logger.info('click =>  page_num:' + str(page_num) + ' current_num:' + str(current_num))

                venue = wait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, 
                    '//*[@id="prod-review"]/div/div[5]/section[4]/div[3]/button[' + str(current_num) +']'
                )))
                logger.info('click: ' + str(page_num))
                #venue.click()
                self.driver.execute_script('arguments[0].click()', venue)
                time.sleep(0.1)

            except NoSuchElementException:
                logger.debug("last page")
                break;
            except TimeoutException:
                logger.debug("button disabled : last page")
                break;
        return
