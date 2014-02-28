import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.options
import time
import base64
from urllib import urlopen


from tornado.ioloop import PeriodicCallback

from session import *
from loadConf import *
from login import *

confAveug = False
ficLog = Login()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        iden = self.get_argument("id","")
        mdp = self.get_argument("mdp","")

        login = Login()
        autorise = login.connexion(iden, mdp)
        print 'maison = httplib.HTTPConnection("192.168.16.150", 80)'
        if autorise == True:
            ficLog.enregDansLog(iden,"Authorized user connection","IP TO DO")
            if confAveug == True:
                print '->Send audio alarm authorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20autorisee")'
            else:
                print '->Send visual alarm authorized user'
                print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->Authorized user access"
            self.set_secure_cookie("user", iden)
            self.redirect("/video")
        else:
            print "->An unauthorized user try to access"
            self.redirect("/unauthorized")

class VideoHandler(BaseHandler):
    def get(self):
        if not self.current_user :
            self.redirect("/")
            return
        self.render("video.html")

class UnauthorizedHandler(BaseHandler):
    def get(self):
        self.render("illegal.html")
    def post(self):
        force = self.get_argument("illegalAccess","")
        if force == "1" :
            self.set_secure_cookie("user", "illegalUser")
            ficLog.enregDansLog("IllegalUser","Unauthorized user connection","IP TO DO")
            if confAveug == True:
                print '->Send audio alarm unauthorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20non%20autorisee")'
            else:
                print '->Send visual alarm unauthorized user'
                print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            self.redirect("/video")
        else :
            self.redirect("/")

class AJAXHandler(BaseHandler):
    def post(self):
        if not self.current_user :
            self.redirect("/")
            return
        try :
            f = urlopen('http://test:a@192.168.1.15/image.jpg?cidx=791836195')
            data = f.read()
            encoded = base64.b64encode(data)
            self.write(encoded)
            self.finish()
        except Exception, e :
            pass

class DisconnectionHandler(BaseHandler):
    def post(self):
        if not self.current_user :
            iden="IllegalUser"
            ficLog.enregDansLog(iden,"Unauthorized user deconnection","IP TO DO")
        else :
            iden = self.current_user
            ficLog.enregDansLog(iden,"Authorized user deconnection","IP TO DO")


        if confAveug == True:
            print '->Send audio alarm deconnection user'
            print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20rompue")'
        else:
            print '->Send visual alarm deconnection user'
            print 'maison.request("GET", "micom/lamp.php?room=salon1&order=0")'
        print"->"+iden+" Deconnection"

        self.set_cookie("user", "0")
        self.redirect("/")

class TestSocket(tornado.websocket.WebSocketHandler):
    def open(self) :
        print "->Websocket opened"
        print '->lol'
        #while 1 :
            try :
                f = urlopen('http://test:a@192.168.1.15/image.jpg?cidx=791836195')
                data = f.read()
                encoded = base64.b64encode(data)
                self.write_message(encoded)
            except tornado.websocket.WebSocketClosedError:
                break
            else :
                self.write_message(" ")
            time.sleep(2)

    def on_message(self,mesg):
        pass

    def on_close(self):
        print "->Websocket closed"


class testHtml(BaseHandler):
    def get(self):
        self.render("test.html")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/video", VideoHandler),
    (r"/unauthorized", UnauthorizedHandler),
    (r"/ajax", AJAXHandler),
    (r"/disconnection", DisconnectionHandler),
    (r"/test", TestSocket),
    (r"/testHtml", testHtml),
], cookie_secret="1213215656")

if __name__ == "__main__":
    hand = LoadConf()
    confAveug = hand.estAveugle()
    if confAveug == True:
        print "->Blind unhabitant system configuration"
    else :
        print "->Not blind unhabitant system configuration"

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()

