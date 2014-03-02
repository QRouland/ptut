import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.options
import time
import base64
import socket

from urllib import urlopen
from tornado.ioloop import PeriodicCallback



from m.loadConf import *
from m.login import *
import os


confAveug = LoadConf().estAveugle()
ficLog = Login()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        self.render("v/index.html")

    def post(self):
        iden = self.get_argument("id","")
        mdp = self.get_argument("mdp","")

        login = Login()
        autorise = login.connexion(iden, mdp)
        print 'maison = httplib.HTTPConnection("192.168.16.150", 80)'
        if autorise == True:
            self.set_secure_cookie("user", iden)
            self.redirect("/video")
        else:
            print "->An unauthorized user try to access"
            self.redirect("/unauthorized")

class VideoHandler(BaseHandler,tornado.websocket.WebSocketHandler):
    def get(self):
        if not self.current_user :
            self.redirect("/")
            return
        self.render("v/video.html")

    def open(self) :
        if not self.current_user :
            self.close()
            return
        print "->Websocket opened"
        if self.current_user == "illegalUser":
            iden="IllegalUser"
            ficLog.enregDansLog(iden,"Unauthorized user connection","IP TO DO")
            if confAveug == True:
                print '->Send audio alarm unauthorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20non%20autorisee")'
            else:
                print '->Send visual alarm unauthorized user'
                print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
        else :
            iden = self.current_user
            ficLog.enregDansLog(iden,"Authorized user connection","IP TO DO")
            if confAveug == True:
                print '->Send audio alarm authorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20autorisee")'
            else:
                print '->Send visual alarm authorized user'
                print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->Authorized user access"
        self.send_image()

    def on_message(self,mesg):
        print "->Data receive"
        self.send_image()

    def on_close(self):
        print "->Websocket closed"
        if self.current_user == "illegalUser":
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

    def send_image(self) :
        try :
            socket.setdefaulttimeout(5)
            f = urlopen('http://test:a@192.168.1.13/image.jpg?cidx=791836195')
            data = f.read()
            encoded = base64.b64encode(data)
            self.write_message(encoded)
            print ("->Data send")
        except Exception, e :
            print e
            self.write_message("error")


class UnauthorizedHandler(BaseHandler):
    def get(self):
        self.render("v/illegal.html")

    def post(self):
        force = self.get_argument("illegalAccess","")
        if force == "1" :
            self.set_secure_cookie("user", "illegalUser")
            self.redirect("/video")
        else :
            self.redirect("/")


class DisconnectionHandler(BaseHandler):
    def post(self):
        if not self.current_user :
            self.close()
            return
        self.clear_cookie("user")
        self.redirect("/")



application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/video", VideoHandler),
    (r"/unauthorized", UnauthorizedHandler),
    (r"/disconnection", DisconnectionHandler),
    (r"/style/(.*)", tornado.web.StaticFileHandler,{"path":"./v/style"},),
    (r"/images/(.*)", tornado.web.StaticFileHandler,{"path":"./v/images"},),
    (r"/js/(.*)", tornado.web.StaticFileHandler,{"path":"./v/js"},)],
    cookie_secret="1213215656")

if __name__ == "__main__":
    if confAveug == True:
        print "->Blind unhabitant system configuration"
    else :
        print "->Not blind unhabitant system configuration"

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
