"""Import Tornado Server"""
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.options
from tornado.ioloop import PeriodicCallback

f = open("requestToMi", "w")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print "lol"


application = tornado.web.Application([
    (r"/lol", MainHandler)])

if __name__ == "__main__":
    try :
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(80)
        tornado.ioloop.IOLoop.instance().start()
    except Exception, e :
        print e
        sys.exit(1)

