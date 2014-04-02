import hashlib


class Login(object):
    """
    Login manager
    """
    def __init__(self,path):
        """
        Define file path for login information
        """
        self.path = path

    def checkLogin(self,pLog,pPasswd):
        """
        Check if login and password are correct (in file fichier/allow)
        password in File are hash (sha224)
        pLog : id login
        pPasswd : password
        return : true if correct login
        false else
        """
        hashPasswd = hashlib.sha224(pPasswd).hexdigest()
        with open(self.path, "r") as source :
            for ligne in source :
                data = ligne.rstrip('\n\r').split(',')
                if data[0] == pLog :
                    if data[1] == hashPasswd :
                        source.close()
                        return True
            source.close()
        return False
