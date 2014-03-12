"""Seveur Tornado"""
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.options
from tornado.ioloop import PeriodicCallback

"""Autre """
import sys
import time
import base64
import socket
import os
from urllib import urlopen

"""Nos Fichier"""
from m.loadConf import *
from m.login import *
from m.log import *


"""Global"""
config = LoadConf()
blind = False
ipCamera = ""
portCamera = ""
portServ =""
log = Log()
urlCamera=""
urlSocket=""



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
        self.set_secure_cookie("user", iden)
        if autorise == True:
            self.set_secure_cookie("user", iden,1)
            self.redirect("/video")
        else:
            log.printL("->An unauthorized user try to access : " + self.request.remote_ip,lvl.WARNING)
            self.redirect("/unauthorized")

class VideoHandler(BaseHandler):
    def get(self):
        if not self.current_user  :
            self.redirect("/")
            return
        self.render("v/video.html", url=urlSocket)

class UnauthorizedHandler(BaseHandler):
    def get(self):
        self.render("v/illegal.html")

    def post(self):
        force = self.get_argument("illegalAccess","")
        if force == "1" :
            self.set_secure_cookie("user", "IllegalUser",1)
            self.redirect("/video")
        else :
            self.redirect("/")


class DisconnectionHandler(BaseHandler):
    def post(self):
        self.clear_cookie("user")
        self.redirect("/")

class WSocketHandler(BaseHandler,tornado.websocket.WebSocketHandler):
    def open(self) :
        if not self.current_user :
            self.close()
            return
        log.printL("->Websocket Open : " + self.request.remote_ip,lvl.SUCCESS)
        iden = self.current_user
        if iden != "IllegalUser":
            log.printL("->"+iden + " : Authorized user connection : "+self.request.remote_ip,lvl.INFO)
            if blind == True:
                log.printL('->Send audio alarm authorized user',lvl.INFO)
                self.send_signal_house('maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20autorisee")')
            else:
                log.printL('->Send visual alarm authorized user',lvl.INFO)
                self.send_signal_house('maison.request("GET", "micom/lamp.php?room=salon1&order=1")')
        else :
            log.printL("->"+iden + ": Unauthorized user connection : " + self.request.remote_ip,lvl.WARNING)
            if blind == True:
                log.printL('->Send audio alarm unauthorized user',lvl.WARNING)
                self.send_signal_house('maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20non%20autorisee")')
            else:
                log.printL('->Send visual alarm unauthorized user',lvl.WARNING)
                self.send_signal_house('maison.request("GET", "micom/lamp.php?room=salon1&order=1")')
        self.send_image()

    def on_message(self,mesg):
        log.printL("->Demand Data Receive : " + self.request.remote_ip,lvl.INFO)
        self.send_image()

    def on_close(self):
        log.printL("->Websocket Closed : "+self.request.remote_ip,lvl.SUCCESS)
        iden = self.current_user
        if iden != "IllegalUser":
            log.printL("->"+iden+" : Authorized User Deconnection : "+self.request.remote_ip,lvl.INFO)
        else :
            log.printL("->"+iden +" : Unauthorized User Deconnection : "+self.request.remote_ip,lvl.WARNING)

        if blind == True:
            log.printL('->Send Audio Alarm Deconnection User', lvl.INFO)
            self.send_signal_house('maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20rompue")')
        else:
            log.printL('->Send Visual Alarm Deconnection User ...',lvl.INFO)
            self.send_signal_house('maison.request("GET", "micom/lamp.php?room=salon1&order=0")')

    def send_signal_house(self, pRq) :
        log.printL('maison = httplib.HTTPConnection("192.168.16.150", 80)',lvl.DEBUG)
        try :
            log.printL('maison.request("GET",'+pRq,lvl.DEBUG)
            log.printL("->Signal To House Send Successfully", lvl.SUCCESS)
        except Exception, e :
            log.printL(e, lvl.FAIL)
            log.printL("->Signal To House Send Failed", lvl.FAIL)

    def send_image(self) :
        try :
            socket.setdefaulttimeout(5)
            f = urlopen(urlCamera)
            data = f.read()
            encoded = base64.b64encode(data)
            self.write_message(encoded)
            log.printL( "->Image Data Send : " + self.request.remote_ip, lvl.INFO)
        except Exception, e :
            log.printL(e,lvl.FAIL)
            self.write_message("error")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/video", VideoHandler),
    (r"/unauthorized", UnauthorizedHandler),
    (r"/disconnection", DisconnectionHandler),
    (r"/socket", WSocketHandler),
    (r"/ssl/(.*)", tornado.web.StaticFileHandler,{"path":"./ssl"},),
    (r"/(favicon.ico)", tornado.web.StaticFileHandler,{"path":"./v/"},),
    (r"/style/(.*)", tornado.web.StaticFileHandler,{"path":"./v/style"},),
    (r"/images/(.*)", tornado.web.StaticFileHandler,{"path":"./v/images"},),
    (r"/js/(.*)", tornado.web.StaticFileHandler,{"path":"./v/js"},)],
    cookie_secret="1213215656")

if __name__ == "__main__":
    log.printL("->Loading configuration ... ",lvl.INFO)
    try :
        blind = config.isBlind()
        ipCamera = config.ipCamera()
        portCamera = config.portCamera()
        ipServ = config.ipServ()
        portServ = config.portServ()
        if blind == "error" :
            raise ConfigError("Failed Load Blind Configuration")
        if ipCamera == "error" :
            raise ConfigError("Failed Load IP Camera Configuration")
        if portCamera == "error" :
            raise ConfigError("Failed Load Port Camera Configuration")
        if ipServ == "error" :
            raise ConfigError("Failed Load IP Server Configuration")
        if portServ == "error" :
            raise ConfigError("Failed Load Port Server Configuration")
    except ConfigError as e :
        log.printL(e.value,lvl.FAIL)
        log.printL("Configuration Loading Failed ! Check Configuration File !",lvl.FAIL)
        sys.exit(1)
    log.printL("->Configuration Server Load Successfully !",lvl.SUCCESS)
    if blind == True:
        log.printL("  +Blind unhabitant",lvl.INFO)
    else :
        log.printL(" +Not blind unhabitant",lvl.INFO)
    log.printL("  +Ip Camera : " + ipCamera,lvl.INFO)
    log.printL("  +Port Camera : " + portCamera,lvl.INFO)
    log.printL("  +Ip Server : " + ipServ,lvl.INFO)
    log.printL("  +Port Server : " + portServ,lvl.INFO)
    print ""

    urlSocket = 'ws://'+ipServ+':'+portCamera+'/socket'
    urlCamera = 'http://test:a@'+ipCamera+':'+portCamera+'/image.jpg?cidx=791836195'

    log.printL("->Ping camera ...",lvl.INFO)
    try :
        socket.setdefaulttimeout(30)
        f = urlopen(urlCamera)
        log.printL( "->Camera OK ", lvl.SUCCESS)
    except Exception, e :
        log.printL("->WARNING : Camera Unreachable! Check Camera Configuration!",lvl.FAIL)
    print ""

    try :
        log.printL("->Server Start ...",lvl.INFO)
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(application,ssl_options={
        "certfile": "/ssl/server.crt",
        "keyfile": "/ssl/server.key",
    })
        })
        http_server.listen(433)
        log.printL("->Server Start Successfully !",lvl.SUCCESS)
        tornado.ioloop.IOLoop.instance().start()
    except Exception, e :
        log.printL("Server Start Failed !",lvl.FAIL)
        sys.exit(1)
