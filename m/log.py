import logging
from logging.handlers import RotatingFileHandler
import time
from datetime import datetime

class Log(object):
    def __init__(self) :
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def enregDansLog(self,pLog,pMsg,pIP):
        with open("fichier/log", "a") as dest :
            d = datetime.now().strftime("%c")
            dest.write("%s,%s,%s,%s\n" % (d,pLog,pMsg,pIP))


    def printL(self,pMsg,pLvl):
        logger.log(pMsg, pLvl)
        if pLvl == 10
            print bcolors.DEBUG ,
        elif pLvl == 20 :
            print bcolors.INFO ,
        elif pLvl == 30 :
            print bcolors.WARNING ,
        elif pLvl == 40 :
            print bcolors.FAIL ,
        print pMsg
        print bcolors.ENDC ,


        }



class bcolors:
    NOTSET = '\033[95m'
    DEBUG = '\033[94m'
    INFO = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''





# création d'un second handler qui va rediriger chaque écriture de log
# sur la console

# Après 3 heures, on peut enfin logguer
# Il est temps de spammer votre code avec des logs partout :
logger.info('Hello')
logger.warning('Testing %s', 'foo')

