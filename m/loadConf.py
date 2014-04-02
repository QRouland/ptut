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
                data = ligne.rstrip('\r\n').split(' ')
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

    def ipCamera(self) :
        """
        Return ipCamera configuration
        Else "error"
        """
        return self.loadValue("camera")

    def portCamera(self) :
        """
        Return portCamera configuration
        Else "error"
        """
        return self.loadValue("portCamera")

    def ipServ(self) :
        """
        Return ipServ configuration
        Else "error"
        """
        return self.loadValue("serv")


    def portServ(self) :
        """
        Return portServ configuration
        Else "error"
        """
        return self.loadValue("portServ")

    def idUrlCamera(self) :
        """
        Return idUrlCamera configuration
        Else "error"
        """
        return self.loadValue("idUrlCamera")

    def endUrlCamera(self) :
        """
        Return endUrlCamera configuration
        Else "error"
        """
        return self.loadValue("endUrlCamera")

    def ipDomo(self) :
        """
        Return ipDomoMi configuration
        Else "error"
        """
        return self.loadValue("ipDomoMi")

    def portDomo(self) :
        """
        Return portDomoMi configuration
        Else "error"
        """
        return self.loadValue("portDomoMi")





class ConfigError(Exception):
    """Exception : error loading configuration"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
