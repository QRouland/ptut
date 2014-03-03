import logging
from logging.handlers import RotatingFileHandler
import time
from datetime import datetime

class Log(object):
    def enregDansLog(self,pLog,pMsg,pIP):
        with open("fichier/log", "a") as dest :
            d = datetime.now().strftime("%c")
            dest.write("%s,%s,%s,%s\n" % (d,pLog,pMsg,pIP))

