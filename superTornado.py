import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.options
import sys
import time
import base64
import socket

from urllib import urlopen
from tornado.ioloop import PeriodicCallback



from m.loadConf import *
from m.login import *
from m.log import *
import os


config = LoadConf()
blind = False
ipCamera = ""
portCamera = ""
portServ =""
log = Log()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_autorisation(self):
        return self.get_secure_cookie("auth")

class MainHandler(BaseHandler):
    def get(self):
        self.render("v/index.html")

    def post(self):
        iden = self.get_argument("id","")
        mdp = self.get_argument("mdp","")

        login = Login()
        autorise = login.connexion(iden, mdp)
        print 'maison = httplib.HTTPConnection("192.168.16.150", 80)'
        self.set_secure_cookie("user", iden)
        if autorise == True:
            self.set_secure_cookie("auth", "yes")
            self.redirect("/video")
        else:
            print "->An unauthorized user try to access : " + self.request.remote_ip
            self.redirect("/unauthorized")

class VideoHandler(BaseHandler):
    def get(self):
        if not self.get_autorisation and not self.get_current_user  :
            self.redirect("/")
            return
        self.render("v/video.html")

class UnauthorizedHandler(BaseHandler):
    def get(self):
        if not self.get_current_user :
            self.redirect("/")
            return
        self.render("v/illegal.html")

    def post(self):
        force = self.get_argument("illegalAccess","")
        if force == "1" :
            self.set_secure_cookie("auth", "no")
            self.redirect("/video")
        else :
            self.redirect("/")


class DisconnectionHandler(BaseHandler):
    def post(self):
        self.clear_cookie("auth")
        self.clear_cookie("user")
        self.redirect("/")

class WSocketHandler(BaseHandler,tornado.websocket.WebSocketHandler):
    def open(self) :
        if not self.get_autorisation and not self.get_current_user :
            self.close()
            return
        print "->Websocket opened : " + self.request.remote_ip
        iden = self.current_user
        if self.get_autorisation == "yes":
            log.enregDansLog(iden,"Authorized user connection",self.request.remote_ip)
            if confAveug == True:
                print '->Send audio alarm authorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20autorisee")'
            else:
                print '->Send visual alarm authorized user'
                print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->Authorized user access : " + self.request.remote_ip
        else :
            log.enregDansLog(iden + " as IllegalUser","Unauthorized user connection",self.request.remote_ip)
            if confAveug == True:
                print '->Send audio alarm unauthorized user'
                print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20non%20autorisee")'
            else:
                print '->Send visual alarm unauthorized user'
                print 'maison.request("GET", "micom/lamp.php?room=salon1&order=1")'
            print "->Unauthorized user access : " + self.request.remote_ip
        self.send_image()

    def on_message(self,mesg):
        print "->Data receive : " + self.request.remote_ip
        self.send_image()

    def on_close(self):
        print "->Websocket closed : "+self.request.remote_ip
        iden = self.current_user
        if self.get_autorisation == "yes":
            log.enregDansLog(iden,"Authorized user deconnection",self.request.remote_ip)
        else :
            log.enregDansLog(iden + " as IllegalUser","Unauthorized user deconnection",self.request.remote_ip)

        if confAveug == True:
            print '->Send audio alarm deconnection user'
            print 'maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20rompue")'
        else:
            print '->Send visual alarm deconnection user'
            print 'maison.request("GET", "micom/lamp.php?room=salon1&order=0")'
        print"->"+iden+" Deconnection : " + self.request.remote_ip


    def send_image(self) :
        try :
            socket.setdefaulttimeout(5)
            f = urlopen('http://test:a@192.168.1.13/image.jpg?cidx=791836195')
            data = f.read()
            encoded = base64.b64encode(data)
            self.write_message(encoded)
            print "->Data send : " + self.request.remote_ip
        except Exception, e :
            print e
            self.write_message("error")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/video", VideoHandler),
    (r"/unauthorized", UnauthorizedHandler),
    (r"/disconnection", DisconnectionHandler),
    (r"/socket", WSocketHandler),
    (r"/style/(.*)", tornado.web.StaticFileHandler,{"path":"./v/style"},),
    (r"/images/(.*)", tornado.web.StaticFileHandler,{"path":"./v/images"},),
    (r"/js/(.*)", tornado.web.StaticFileHandler,{"path":"./v/js"},)],
    cookie_secret="1213215656")

if __name__ == "__main__":
    log.printL("->Loading configuration ... ",20)
    try :
        blind = config.isBlind()
        ipCamera = config.ipCamera()
        portCamera = config.portCamera()
        portServ = config.portServ()
        if blind == "error" :
            raise ConfigError("Failed Load Blind Configuration")
        if ipCamera == "error" :
            raise ConfigError("Failed Load IP Camera Configuration")
        if portCamera == "error" :
            raise ConfigError("Failed Load IP Camera Configuration")
        if portServ == "error" :
            raise ConfigError("Failed Load Port Server Configuration")
    except ConfigError as e :
        log.printL(e.value,40)
        log.printL("Configuration Loading Failed ! Check Configuration File !",40)
        sys.exit(1)
    print log.printL("->Configuration Server Load Successfully !",25)
    if blind == True:
        log.printL("  +Blind unhabitant",20)
    else :
        log.printL(" +Not blind unhabitant",20)
    log.printL("  +Ip Camera : " + ipCamera,20)
    log.printL("  +Port Camera : " + portCamera,20)
    log.printL("  +Port Server : " + portServ,20)
    print ""

    try :
        log.printL("->Server Start ...",20)
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(portServ)
        log.printL("->Server Start Successfully !",25)
        tornado.ioloop.IOLoop.instance().start()
    except Exception, e :
        log.printL("Server Start Failed !",40)
        log.printL(e.value,40)
        sys.exit(1)
