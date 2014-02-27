import tornado.ioloop
import tornado.web
import tornado.httpserver

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        #iden = self.get_argument("id",'')
        #mdp = self.get_argument("mdp",'')
        self.write("Le pseudo est :")




application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
