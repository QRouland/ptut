import logging
from logging.handlers import RotatingFileHandler

class bcolors:
    DEBUG = '\033[94m'
    INFO = '\033[95m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class lvl:
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    FAIL = 40

class Log(object):
    def __init__(self) :

        logging.addLevelName(lvl.SUCCESS, "SUCCESS")

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
        steam_handler.setLevel(logging.NOTSET)
        self.logger.addHandler(steam_handler)


    def printL(self,pMsg,pLvl):
        if pLvl == lvl.DEBUG :
            pMsg = bcolors.DEBUG + pMsg + bcolors.ENDC
        elif pLvl == lvl.INFO :
            pMsg = bcolors.INFO + pMsg + bcolors.ENDC
        elif pLvl == lvl.SUCESS :
            pMsg = bcolors.SUCCESS + pMsg + bcolors.ENDC
        elif pLvl == lvl.WARNING :
            pMsg = bcolors.WARNING + pMsg + bcolors.ENDC
        elif pLvl == lvl.FAIL :
            pMsg = bcolors.FAIL + pMsg + bcolors.ENDC
        self.logger.log(pLvl,pMsg)







