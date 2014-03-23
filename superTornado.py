"""Import Tornado Server"""
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.options
from tornado.ioloop import PeriodicCallback

"""Other imports """
import sys
import time
import base64
import socket
import os
from urllib import urlopen
import string
import random

"""Import files"""
from m.loadConf import *
from m.login import *
from m.log import *


class GlobalVars :
    """
    Global vars for server
    """
    config = LoadConf()
    blind = False
    ipCamera = ""
    portCamera = ""
    endUrlCamera = ""
    idCamera = ""
    urlCamera = ""
    portServ = ""
    log = Log()
    urlSocket = ""
    authorized = 0
    unauthorized = 0



class BaseHandler(tornado.web.RequestHandler):
    """
    Define BaseHandler for create the basis for session connection
    cookie secure  based (sign and timestamp )
    """
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    """
    Main web page : / in http sever
    """
    def get(self):
        """
        GET request -> return index.html where user can login
        """
        self.render("v/index.html")

    def post(self):
        """
        POST request -> try to connect user with parameter POST (iden and paswd)
        if connection sucessfull
            go to the /video page (VideoHandler)
        else
            go to the /unauthorized page (UnauthorizedHandler)
        """
        iden = self.get_argument("id","")
        paswd = self.get_argument("paswd","")

        login = Login()
        autorise = login.checkLogin(iden, paswd)
        self.set_secure_cookie("user", iden)
        if autorise == True:
            self.set_secure_cookie("user", iden,1)
            self.redirect("/video")
        else:
            GlobalVars.log.printL("->An unauthorized user try to access : " + self.request.remote_ip,lvl.WARNING)
            self.redirect("/unauthorized")


class VideoHandler(BaseHandler):
    """
    Video web page : /video in http sever
    """
    def get(self):
        """
        GET request ->
        If user is connected return video.html who
            allow with websocket (WSocketHandler) to see the video of the camera
        Else
            go to main page (MainHandler)
        """
        if not self.current_user  :
            self.redirect("/")
            return
        self.render("v/video.html", url=GlobalVars.urlSocket)


class UnauthorizedHandler(BaseHandler):
    """
    Unauthorized web page : /unauthorized in http server
    """
    def get(self):
        """
        GET request -> show the illegal.html page
        """
        self.render("v/illegal.html")

    def post(self):
        """
        POST request ->
        if parameter POST force == 1
            force acess to camera
        else
             go to / page (MainHandler)
        """
        force = self.get_argument("illegalAccess","")
        if force == "1" :
            self.set_secure_cookie("user", "IllegalUser",1)
            self.redirect("/video")
        else :
            self.redirect("/")


class DisconnectionHandler(BaseHandler):
    """
    /disconnection in http server
    """
    def get(self):
        """
        GET request -> clear session : disconnect user
        """
        self.clear_cookie("user")
        self.redirect("/")


class WSocketHandler(BaseHandler,tornado.websocket.WebSocketHandler):
    """
    /socket in http server
    websocket definition
    """
    def open(self) :
        """
        Open socket request ->
        if is a connect user
            open connection socket, alert the unhabitant with the good signal
        else
            don't open connection
        """
        if not self.current_user :
            self.close()
            return
        GlobalVars.log.printL("->Websocket Open : " + self.request.remote_ip,lvl.SUCCESS)
        iden = self.current_user
        if iden != "IllegalUser":
            GlobalVars.log.printL("->"+iden + " : Authorized user connection : "+self.request.remote_ip,lvl.INFO)
            if GlobalVars.blind == True:
                GlobalVars.authorized + 1
                GlobalVars.log.printL('->Send audio alarm authorized user',lvl.INFO)
                self.send_signal_house('maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20autorisee")')
            else:
                GlobalVars.authorized + 1
                GlobalVars.log.printL('->Send visual alarm authorized user',lvl.INFO)
                self.send_signal_house('maison.request("GET", "micom/lamp.php?room=salon1&order=1")')
        else :
            GlobalVars.log.printL("->"+iden + ": Unauthorized user connection : " + self.request.remote_ip,lvl.WARNING)
            if GlobalVars.blind == True:
                GlobalVars.unauthorized + 1
                GlobalVars.log.printL('->Send audio alarm unauthorized user',lvl.WARNING)
                self.send_signal_house('maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20non%20autorisee")')
            else:
                GlobalVars.unauthorized + 1
                GlobalVars.log.printL('->Send visual alarm unauthorized user',lvl.WARNING)
                self.send_signal_house('maison.request("GET", "micom/lamp.php?room=salon1&order=1")')
        self.send_image()


    def on_message(self,mesg):
        """
        Client Ask For Image
        """
        GlobalVars.log.printL("->Demand Data Receive : " + self.request.remote_ip,lvl.INFO)
        self.send_image()

    def on_close(self):
        """
        Socket connection Connection->
        Alert unhabitant with the good signal
        """
        GlobalVars.log.printL("->Websocket Closed : "+self.request.remote_ip,lvl.SUCCESS)
        iden = self.current_user
        if iden != "IllegalUser":
            GlobalVars.authorized - 1
            GlobalVars.log.printL("->"+iden+" : Authorized User Deconnection : "+self.request.remote_ip,lvl.INFO)
        else :
            GlobalVars.unauthorized - 1
            GlobalVars.log.printL("->"+iden +" : Unauthorized User Deconnection : "+self.request.remote_ip,lvl.WARNING)

        if GlobalVars.blind == True:
            if (GlobalVars.unauthorized == 0) and (GlobalVars.authorized == 0):
                GlobalVars.log.printL('->Send Audio Alarm Deconnection User', lvl.INFO)
                self.send_signal_house('maison.request("GET", "micom/say.php?source=toto&text=Connection%20a%20la%20camera%20rompue")')
        else:
            if (GlobalVars.unauthorized == 0) and (GlobalVars.authorized == 0):
                GlobalVars.log.printL('->Send Visual Alarm Deconnection User ...',lvl.INFO)
                self.send_signal_house('maison.request("GET", "micom/lamp.php?room=salon1&order=0")')

    def send_signal_house(self, pRq) :
        """
        Allow send pRq request to the house
        """
        GlobalVars.log.printL('maison = httplib.HTTPConnection("192.168.16.150", 80)',lvl.DEBUG)
        try :
            GlobalVars.log.printL('maison.request("GET",'+pRq,lvl.DEBUG)
            GlobalVars.log.printL("->Signal To House Send Successfully", lvl.SUCCESS)
        except Exception, e :
            GlobalVars.log.printL(e, lvl.FAIL)
            GlobalVars.log.printL("->Signal To House Send Failed", lvl.FAIL)

    def send_image(self) :
        """
        Allow send the image in the websocket
        """
        try :
            socket.setdefaulttimeout(5)
            f = urlopen(GlobalVars.urlCamera)
            data = f.read()
            encoded = base64.b64encode(data)
            f.close()
            self.write_message(encoded)
            GlobalVars.log.printL( "->Image Data Send : " + self.request.remote_ip, lvl.INFO)
        except Exception, e :
            GlobalVars.log.printL(e,lvl.FAIL)
            self.write_message("error")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/video", VideoHandler),
    (r"/unauthorized", UnauthorizedHandler),
    (r"/disconnection", DisconnectionHandler),
    (r"/socket", WSocketHandler),
    (r"/(favicon.ico)", tornado.web.StaticFileHandler,{"path":"./v/images"},),
    (r"/style/(.*)", tornado.web.StaticFileHandler,{"path":"./v/style"},),
    (r"/images/(.*)", tornado.web.StaticFileHandler,{"path":"./v/images"},),
    (r"/js/(.*)", tornado.web.StaticFileHandler,{"path":"./v/js"},)],
    cookie_secret=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64)))

if __name__ == "__main__":
    GlobalVars.log.printL("->Loading configuration ... ",lvl.INFO)
    try :
        GlobalVars.blind = GlobalVars.config.isBlind()
        GlobalVars.ipCamera = GlobalVars.config.ipCamera()
        GlobalVars.portCamera = GlobalVars.config.portCamera()
        GlobalVars.idUrlCamera = GlobalVars.config.idUrlCamera()
        GlobalVars.endUrlCamera = GlobalVars.config.endUrlCamera()
        GlobalVars.ipServ = GlobalVars.config.ipServ()
        GlobalVars.portServ = GlobalVars.config.portServ()

        if GlobalVars.blind == "error" :
            raise ConfigError("Failed Load Blind Configuration")
        if GlobalVars.ipCamera == "error" :
            raise ConfigError("Failed Load IP Camera Configuration")
        if GlobalVars.portCamera == "error" :
            raise ConfigError("Failed Load Port Camera Configuration")
        if GlobalVars.idUrlCamera == "error" :
            raise ConfigError("Failed Load ID Camera Configuration")
        if GlobalVars.endUrlCamera == "error" :
            raise ConfigError("Failed Load End Url  Camera Configuration")
        if GlobalVars.ipServ == "error" :
            raise ConfigError("Failed Load IP Server Configuration")
        if GlobalVars.portServ == "error" :
            raise ConfigError("Failed Load Port Server Configuration")
    except ConfigError as e :
        GlobalVars.log.printL(e.value,lvl.FAIL)
        GlobalVars.log.printL("Configuration Loading Failed ! Check Configuration File !",lvl.FAIL)
        sys.exit(1)
    GlobalVars.log.printL("->Configuration Server Load Successfully !",lvl.SUCCESS)
    if GlobalVars.blind == True:
        GlobalVars.log.printL("  +Blind unhabitant",lvl.INFO)
    else :
        GlobalVars.log.printL(" +Not blind unhabitant",lvl.INFO)
    GlobalVars.log.printL("  +Ip Camera : " + GlobalVars.ipCamera,lvl.INFO)
    GlobalVars.log.printL("  +Port Camera : " + GlobalVars.portCamera,lvl.INFO)
    GlobalVars.log.printL("  +ID url Camera : " + GlobalVars.idUrlCamera,lvl.INFO)
    GlobalVars.log.printL("  +End url Camera : " + GlobalVars.endUrlCamera,lvl.INFO)
    GlobalVars.log.printL("  +Ip Server : " + GlobalVars.ipServ,lvl.INFO)
    GlobalVars.log.printL("  +Port Server : " + GlobalVars.portServ,lvl.INFO)
    print ""

    GlobalVars.urlSocket = 'ws://'+GlobalVars.ipServ+':'+GlobalVars.portCamera+'/socket'
    GlobalVars.urlCamera = 'http://'+GlobalVars.idUrlCamera+'@'+GlobalVars.ipCamera+':'+GlobalVars.portCamera+GlobalVars.endUrlCamera

    GlobalVars.log.printL("->Ping camera ...",lvl.INFO)
    try :
        socket.setdefaulttimeout(30)
        urlopen(GlobalVars.urlCamera)
        GlobalVars.log.printL( "->Camera OK ", lvl.SUCCESS)
    except Exception, e :
        GlobalVars.log.printL("->WARNING : Camera Unreachable! Check Camera Configuration!",lvl.FAIL)
    print ""

    try :
        GlobalVars.log.printL("->Server Start ...",lvl.INFO)
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(GlobalVars.portServ)
        GlobalVars.log.printL("->Server Start Successfully !",lvl.SUCCESS)
        tornado.ioloop.IOLoop.instance().start()
    except Exception, e :
        GlobalVars.log.printL("Server Start Failed !",lvl.FAIL)
        sys.exit(1)
