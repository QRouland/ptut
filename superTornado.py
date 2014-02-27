import tornado.httpserver
import tornado.ioloop





def main(port = 80):
    ioloop = tornado.ioloop.IOLoop.instance()
    application = tornado.web.Application([
    (r"/get/(sysinfo|cpuinfo)", InfoHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    try:
        ioloop.start()
    except KeyboardInterrupt:
        pass


