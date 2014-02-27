import tornado.ioloop
import tornado.web
import tornado.httpserver
from loadConf import *
from login import *

confAveug = False
ficLog = Login()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        iden = self.get_argument("id","")
        mdp = self.get_argument("mdp","")

        login = Login()
        autorise = login.connexion(iden, mdp)
        # maison = httplib.HTTPConnection("192.168.16.150", 80)
        if autorise == True:
            ficLog.enregDansLog(iden,"Authorized user connection",info[0])
            if confAveug == True:
                print '->Send audio alarm authorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20autorisee")'
            else:
                print '->Send visual alarm authorized user'
                print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->Send to client authorized user access"
            # redirection autorisé

            else:
            ficLog.enregDansLog(iden,"Unauthorized user connection",info[0])
            if confAveug == True:
                print '->Send audio alarm unauthorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20non%20autorisee")'
            else:
                    print '->Send visual alarm unauthorized user'
                    print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->Send to client unauthorized user access"
            # redirection non autorisé





application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/video", VideoHandler),
    (r"/authorized", VideoHandler),
])

if __name__ == "__main__":
    # chargement congfig
    hand = LoadConf()
    confAveug = hand.estAveugle()
    if confAveug == True:
        print "->Blind unhabitant system configuration"
    else :
        print "->Not blind unhabitant system configuration"

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
