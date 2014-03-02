class LoadConf(object):
    def loadValue(self, key):
        with open("m/fichier/conf", "r") as source :
            for ligne in source:
                data = ligne.rstrip('\n\r').split('=')
                if data[0] in key :
                        source.close()
                        return data[1]
            source.close()
        return "error"

    def isBlind(self):
        rep = self.loadValue("blind")
        if rep == "1" :
            return True
        else if rep == "0":
            return False
        else :
            return rep

    def ipCamera(self)
        return self.loadValue("camera")

    def portServ(self)
        return self.loadValue("port")
