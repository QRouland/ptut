import logging
from logging.handlers import RotatingFileHandler
import time
from datetime import datetime

class Log(object):
    def __init__(self) :
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler('m/fichier/log', 'a', 1000000, 1)

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


        self.steam_handler = logging.StreamHandler()
        self.steam_handler.setLevel(logging.DEBUG)
        logger.addHandler(steam_handler)


    def printL(self,pMsg):
        self.logger.info(pMsg)
