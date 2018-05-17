#!/usr/bin/env python

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Crimson():
    def __init__(self):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chromeOptions.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(
            executable_path='/usr/bin/chromedriver'
            , chrome_options=chromeOptions)

    def end(self):
        self.driver.implicitly_wait(30)
        self.driver.quit()
    
    def test_crimson(self):
        driver = self.driver
        driver.get("https://forsight.crimsonhexagon.com/ch/login")
        driver.implicitly_wait(3)
        #driver.find_element_by_id("emailAddress").clear()
        driver.find_element_by_id("emailAddress").send_keys("xxxx@xxxx.com")
        driver.find_element_by_xpath("//button[@id='next']/span").click()
        #driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("yyyyyy")
        driver.find_element_by_xpath("//div[@id='loginStep2']/form/fieldset/button/span").click()
        driver.find_element_by_xpath("//div[4]/div/div/div/div[2]/div[2]").click()
        driver.find_element_by_xpath("//nav[@id='global-nav-header']/div[3]/div/div/div").click()
        driver.find_element_by_xpath("//nav[@id='global-nav-header']/div[3]/div/div/ul/li/span").click()
        #driver.find_element_by_xpath("//a[@id='forsight']/div[3]").click()
        driver.find_element_by_xpath("//*[@id='forsight']").click()
        driver.find_element_by_id("newMonitor").click()
        driver.find_element_by_xpath("//form[@id='monitorSetup']/ul/li/div[2]/h2").click()
        driver.find_element_by_name("name").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("test_monitor")
      
        time.sleep(1)

        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[1]/div/div[1]/span").click()
        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[1]/div/div[1]/span").click()
        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[2]/div/div[1]/span").click()
        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[3]/div/div[1]/span").click()
        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[4]/div/div[1]/span").click()
        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[5]/div/div[1]/span").click()
        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[6]/div/div[1]/span").click()
        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[7]/div/div[1]/span").click()
        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[8]/div/div[1]/span").click()
        driver.find_element_by_xpath("//*[@id='monitorSetup']/div[2]/div/div/div[2]/div/div/div[1]/ul/li[9]/div/div[1]/span").click()

        driver.find_element_by_xpath("//form[@id='monitorSetup']/div[3]/div[2]/ul/li[2]/span").click()
        
        driver.find_element_by_xpath("//*[@id='advanced-keywords']/div[2]/div").click()
        x = driver.switch_to.active_element
        time.sleep(1)
        x.send_keys(Keys.RETURN)
        x.send_keys("feature_keyword_ex1")

        driver.find_element_by_css_selector('input[class="datepicker datepicker-start hasDatepicker"]').click();
        driver.find_element_by_xpath("//*[@id='ui-datepicker-div']/div/div/select[1]").click();
        driver.find_element_by_link_text("1").click()

        driver.find_element_by_id("button-create").click()
    
if __name__ == "__main__":
    driver = Crimson()
    driver.test_crimson();
    driver.end();
