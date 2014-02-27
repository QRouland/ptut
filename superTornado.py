import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        iden = self.get_argument("id",'')
        mdp = self.get_argument("mdp",'')
        self.write("Le pseudo est :", iden)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPSERVER(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
