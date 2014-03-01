class LoadConf(object):
    def loadHand(self):
        with open("m/fichier/conf", "r") as source :
            for ligne in source:
                data = ligne.rstrip('\n\r').split('=')
                if data[0] in 'handicap' :
                        source.close()
                        return data[1]
            source.close()
        return 0

    def estAveugle(self):
        if self.loadHand() == "1" :
            return True
        else :
            return False
