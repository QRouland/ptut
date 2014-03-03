import hashlib
import httplib


class Login(object):
    def verifLogin(self,pLog,pMdp):
        hashMdp = hashlib.sha224(pMdp).hexdigest()
        with open("m/fichier/autorise", "r") as source :
            for ligne in source :
                data = ligne.rstrip('\n\r').split(',')
                if data[0] == pLog :
                    if data[1] in hashMdp :
                        source.close()
                        return True
            source.close()
        return False

    def connexion(self,pLog,pMdp):
        if self.verifLogin(pLog,pMdp) == True :
            return True
        else :
            return False









