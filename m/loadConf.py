class LoadConf(object):
    def loadValue(self, key):
        with open("m/fichier/conf", "r") as source :
            for ligne in source:
                data = ligne.rstrip('\n\r').split('=')
                try :
                    if data[0] in key :
                            source.close()
                            return data[1]
                except Exception, e :
                    pass
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

    def portServ(self) :
        return self.loadValue("portServ")

class ConfigError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
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


