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
import re
import time
import os
import os.path
import datetime
import pandas as pd
import numpy as np
import validators

CH_URL = 'https://forsight.crimsonhexagon.com/ch/login';

LOG_FILE = './log.txt';
logger = logging.getLogger('mylogger');

class CrimsonHexagon:

    def __init__(self):

        # debug info warning error critical
        logger.setLevel(logging.INFO)
        fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

        fileHandler = logging.FileHandler(LOG_FILE)
        logger.addHandler(fileHandler)
        fileHandler.setFormatter(fomatter)

        self.current_url = None
        self.user = None
        self.pwd = None
        logger.info("Creating crawler is done.")

    def openPage(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(3)
            self.current_url = url
        except:
            logger.error("driver get excepttion")
        return  

    def init(self, user, pwd):

        self.user = user;
        self.pwd = pwd;

        #logger.info("user[%s] pwd[%s]" % (user, pwd) )
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chromeOptions.add_experimental_option("prefs",prefs)

        self.driver = webdriver.Chrome(
            executable_path='/usr/bin/chromedriver'
            , chrome_options=chromeOptions)

        #self.driver = webdriver.PhantomJS()

        self.openPage(CH_URL);

        logger.info("Initialize complete.")

    def end(self):
        self.driver.quit()
        logger.info("Done !!!!")

    def login(self):

        # Send user,pwdto web
        USER_INPUT_CSS = 'input[class="focusOnMe"]';
        user = self.driver.find_element_by_css_selector(USER_INPUT_CSS)
        user.send_keys(self.user)
        user.send_keys(Keys.RETURN)

        PWD_INPUT_CSS = 'input[id="password"]';
        user = self.driver.find_element_by_css_selector(PWD_INPUT_CSS)
        user.send_keys(self.pwd)
        user.send_keys(Keys.RETURN)
        #time.sleep(1)

        logger.info('enter username and password')
        try:
            logger.info("wait start")
            venue = wait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
                    '/html/body/div[4]/div/div/div/div[2]/div[2]'
            )))
            logger.info("wait success")
            venue.click()
            #self.driver.execute_script('arguments[0].click()', venue)
            logger.info("click")
        except NoSuchElementException:
            logger.info("wait fail")
            logger.info("No such element")
        except TimeoutException:
            logger.info("wait fail")
            logger.info("Timeout")

        logger.info('click skip button')
        
        time.sleep(1000)
