import hashlib
import httplib


class Login(object):
    """
    Login manager
    """
    def checkLogin(self,pLog,pPasswd):
        """
        Check if login and password are correct (in file fichier/allow)
        password in File are hash (sha224)
        pLog : id login
        pPasswd : password
        return : true if correct login
        false else
        """
        hashMdp = hashlib.sha224(pPasswd).hexdigest()
        with open("m/fichier/allow", "r") as source :
            for ligne in source :
                data = ligne.rstrip('\n\r').split(',')
                if data[0] == pLog :
                    if data[1] == hashMdp :
                        source.close()
                        return True
            source.close()
        return False









