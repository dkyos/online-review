#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
from crimson_crawler import CrimsonHexagon

if __name__ == "__main__":

    driver = CrimsonHexagon()

    driver.init('xxx@xxx.com', 'yyyyy')

    driver.login()

    #driver.create_monitor()

    driver.end()
