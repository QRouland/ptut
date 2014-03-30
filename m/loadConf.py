class LoadConf(object):
    """Loading configuration file"""

    def __init__(self,path):
        """
        Define file path for load config
        """
        self.path = path

    def loadValue(self, key):
        """
        Return the value associate to the key into conf file (fichier/conf)
        Else return "error"
        """
        with open(self.path , "r") as source :
            for ligne in source:
                data = ligne.rstrip('\r\n').split('=')
                if data[0] == key :
                    source.close()
                    return data[1]
            source.close()
        return "error"

    def isBlind(self):
        """
        Return true if configuration is for Blind
        Else false
        """
        rep = self.loadValue("blind")
        if rep == "1" :
            return True
        elif rep == "0":
            return False
        else :
            return rep

    """
    Return ipCamera configuration
    Else "error"
    """
    def ipCamera(self) :
        return self.loadValue("camera")

    """
    Return portCamera configuration
    Else "error"
    """
    def portCamera(self) :
        return self.loadValue("portCamera")

    """
    Return ipServ configuration
    Else "error"
    """
    def ipServ(self) :
        return self.loadValue("serv")

    """
    Return portServ configuration
    Else "error"
    """
    def portServ(self) :
        return self.loadValue("portServ")

    """
    Return idUrlCamera configuration
    Else "error"
    """
    def idUrlCamera(self) :
        return self.loadValue("idUrlCamera")

    """
    Return endUrlCamera configuration
    Else "error"
    """
    def endUrlCamera(self) :
        return self.loadValue("endUrlCamera")
    """
    Return ipDomoMi configuration
    Else "error"
    """
    def ipDomo(self) :
        return self.loadValue("ipDomoMi")
    """
    Return portDomoMi configuration
    Else "error"
    """
    def portDomo(self) :
        return self.loadValue("portDomoMi")





class ConfigError(Exception):
    """Exception : error loading configuration"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)




