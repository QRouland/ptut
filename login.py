import time
import hashlib
import httplib
from datetime import datetime

class Login(object):
    def verifLogin(self,pLog,pMdp):
        hashMdp = hashlib.sha224(pMdp).hexdigest()
        with open("fichier/autorise", "r") as source :
            for ligne in source :
                data = ligne.rstrip('\n\r').split(',')
                if data[0] in pLog :
                    if data[1] in hashMdp :
                        source.close()
                        return True
            source.close()
        return False

    def enregDansLog(self,pLog,pMsg,pIP):
        with open("fichier/log", "a") as dest :
            d = datetime.now().strftime("%c")
            dest.write("%s,%s,%s,%s\n" % (d,pLog,pMsg,pIP))

    def connexion(self,pLog,pMdp):
        if self.verifLogin(pLog,pMdp) == True :
            return True
        else :
            return False









