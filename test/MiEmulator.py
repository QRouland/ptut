"""Import Tornado Server"""
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.options
from tornado.ioloop import PeriodicCallback

f = open("requestToMi", "w")

class SayHandler(tornado.web.RequestHandler):
    def get(self):
        source = self.get_argument("source","")
        text = self.get_argument("text","")
        print"/micom/say.php?source=" + source + "&text=" + text


class LampHandler(tornado.web.RequestHandler):
    def get(self):
        room = self.get_argument("room","")
        order = self.get_argument("order","")
        print"/micom/lamp.php?room=" + room + "&order=" + order



application = tornado.web.Application([
    (r"/micom/say.php", SayHandler),
    (r"/micom/lamp.php", LampHandler)])

if __name__ == "__main__":
    try :
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except Exception, e :
        print e
        sys.exit(1)

