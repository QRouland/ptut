import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket

from tornado.ioloop import PeriodicCallback

from session import *
from loadConf import *
from login import *

confAveug = False
ficLog = Login()
session= TornadoSessionManager()
settings = {}
settings["session_secret"] = 'some secret password!!'
settings["session_dir"] = 'sessions'  # the directory to store sessions in
session= Session()
application.session_manager = session.TornadoSessionManager(settings["session_secret"], settings["session_dir"])

class MainHandler(tornado.web.RequestHandler):
    def __init__ (self) :
        self.session = session.TornadoSession(self.application.session_manager, self)
    def get(self):
        self.render("index.html")
    def post(self):
        iden = self.get_argument("id","")
        mdp = self.get_argument("mdp","")

        login = Login()
        autorise = login.connexion(iden, mdp)
        #maison = httplib.HTTPConnection("192.168.16.150", 80)
        if autorise == True:
            ficLog.enregDansLog(iden,"Authorized user connection","IP TO DO")
            if confAveug == True:
                print '->Send audio alarm authorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20autorisee")'
            else:
                print '->Send visual alarm authorized user'
                print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->Send to client authorized user access"
            self.session['blah'] = 1234
            self.save()
            blah = self.session['blah']
            self.write(blah)

        else:
            ficLog.enregDansLog(iden,"Unauthorized user connection","IP TO DO")
            if confAveug == True:
                print '->Send audio alarm unauthorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20non%20autorisee")'
            else:
                    print '->Send visual alarm unauthorized user'
                    print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->Send to client unauthorized user access"
            self.write("Unauthorized user access")

class VideoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}

    def on_message(self, message):
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        print "Client %s received a message : %s" % (self.id, message)

    def on_close(self):
        if self.id in clients:
            del clients[self.id]


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/video", VideoHandler),
    (r"/test", WSHandler),
])

if __name__ == "__main__":
    hand = LoadConf()
    confAveug = hand.estAveugle()
    if confAveug == True:
        print "->Blind unhabitant system configuration"
    else :
        print "->Not blind unhabitant system configuration"

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()

