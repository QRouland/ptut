import logging
from logging.handlers import RotatingFileHandler

class bcolors:
    """
    Define constant value color for different level
    """
    DEBUG = '\033[94m'
    INFO = '\033[95m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class lvl:
    """
    Define constant value for level log
    """
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    FAIL = 40

class SingleLevelFilter(logging.Filter):
    """Filter for one level"""
    def __init__(self, passlevel, reject):
        """
        Constructor
        passlevel : level to filter
        reject : true on reject state
        """
        self.passlevel = passlevel
        self.reject = reject
    def filter(self, record):
         if self.reject:
             return (record.levelno != self.passlevel)
         else:
             return (record.levelno == self.passlevel)

class Log(object):
    """
    Log Manager
    """
    def __init__(self) :
        """
        Define 3 differents log :
        activity.log -> all activity server
        warning.log -> only warning server (including illegal acess)
        error.log' -> error server
        Write all message on terminal too
        """
        logging.addLevelName(lvl.SUCCESS, "SUCCESS")

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-15s :: %(levelname)s :: %(message)s')

        file_handler = RotatingFileHandler('log/activity.log', 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        file_handler_warning = RotatingFileHandler('log/warning.log', 'a', 1000000, 1)
        f1 = SingleLevelFilter(logging.WARNING, False)
        file_handler_warning.addFilter(f1)
        file_handler_warning.setFormatter(formatter)
        self.logger.addHandler(file_handler_warning)

        file_handler_error = RotatingFileHandler('log/error.log', 'a', 1000000, 1)
        file_handler_error.setLevel(logging.ERROR)
        file_handler_error.setFormatter(formatter)
        self.logger.addHandler(file_handler_error)

        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(logging.NOTSET)
        self.logger.addHandler(steam_handler)


    def printL(self,pMsg,pLvl):
        """
        Add color and write in log with an define level
        pMsg : message to write in log
        pLvl : level of log message
        """
        if pLvl == lvl.DEBUG :
            pMsg = bcolors.DEBUG + str(pMsg) + bcolors.ENDC
        elif pLvl == lvl.INFO :
            pMsg = bcolors.INFO + str(pMsg) + bcolors.ENDC
        elif pLvl == lvl.SUCCESS :
            pMsg = bcolors.SUCCESS + str(pMsg) + bcolors.ENDC
        elif pLvl == lvl.WARNING :
            pMsg = bcolors.WARNING + str(pMsg) + bcolors.ENDC
        elif pLvl == lvl.FAIL :
            pMsg = bcolors.FAIL + str(pMsg) + bcolors.ENDC
        self.logger.log(pLvl,pMsg)







