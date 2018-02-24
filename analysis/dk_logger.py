#-*- coding: utf-8 -*-

import logging
import os

class SingletonInstance:
    __instance = None

    @classmethod
    def __getInstance(cls):
        #print("3. __getInstance called of SingletonInstance")
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        #print("1. instance called of SingletonInstance")
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class dk_logger(SingletonInstance):
    _logger = None

    def __init__(self):
        #print("2. __init__ called of dk_logger")
        self._logger = logging.getLogger("myLogger")
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

        import datetime
        now = datetime.datetime.now()
        import time
        timestamp = time.mktime(now.timetuple())

        dirname = './log'
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        fileHandler = logging.FileHandler(dirname + "/"+now.strftime("%Y-%m-%d_%H-%M-%S")+".log")
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

    def set_logger_debug(self):
        self._logger.setLevel(logging.DEBUG)
        return

    def get_logger():
        self = dk_logger.instance()
        return self._logger

