import logging
from logging.handlers import RotatingFileHandler
import sys
import time
from datetime import datetime

class Log(object):
    def __init__(self) :

        logging.addLevelName(25, "SUCCESS")

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-15s :: %(levelname)s :: %(message)s')

        file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        file_handler_error = RotatingFileHandler('error.log', 'a', 1000000, 1)
        file_handler_error.setLevel(logging.ERROR)
        file_handler_error.setFormatter(formatter)
        self.logger.addHandler(file_handler_error)

        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(steam_handler)

    def enregDansLog(self,pLog,pMsg,pIP):
        with open("fichier/log", "a") as dest :
            d = datetime.now().strftime("%c")
            dest.write("%s,%s,%s,%s\n" % (d,pLog,pMsg,pIP))


    def printL(self,pMsg,pLvl):
        if pLvl == 10 :
            sys.stdout.write(bcolors.DEBUG)
        elif pLvl == 20 :
            sys.stdout.write(bcolors.INFO)
        elif pLvl == 25 :
            sys.stdout.write(bcolors.SUCCESS)
        elif pLvl == 30 :
            sys.stdout.write(bcolors.WARNING)
        elif pLvl == 40 :
            sys.stdout.write(bcolors.FAIL)
        self.logger.log(pLvl,pMsg)
        sys.stdout(bcolors.ENDC)

class bcolors:
    DEBUG = '\033[94m'
    INFO = '\033[95m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'




