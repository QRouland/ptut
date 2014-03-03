class LoadConf(object):
    def loadValue(self, key):
        with open("m/fichier/conf", "r") as source :
            for ligne in source:
                data = ligne.rstrip('\n\r').split('=')
                if data[0] == key :
                    source.close()
                    return data[1]
            source.close()
        return "error"

    def isBlind(self):
        rep = self.loadValue("blind")
        if rep == "1" :
            return True
        elif rep == "0":
            return False
        else :
            return rep

    def ipCamera(self) :
        return self.loadValue("camera")

    def portCamera(self) :
        return self.loadValue("portCamera")

    def ipServ(self) :
        return self.loadValue("serv")

    def portServ(self) :
        return self.loadValue("portServ")

class ConfigError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)




