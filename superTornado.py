import markdown
import os.path
import re
import tornado.auth
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1", help="api database host")
define("mysql_database", default="tornado_api", help="tornado_api database name")
define("mysql_user", default="root", help="tornado_api database user")
define("mysql_password", default="", help="tornado_api database password")


class Application(tornado.web.Application):
    def __init__(self):
        project_dir = './site'

        handlers = [
            (r"/all_book/", BooksHandler),
            (r"/all_category/", CategoryHandler),
        ]
        settings = dict(
            #autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class BooksHandler(BaseHandler):
    def post(self):
        try:
            print "Adding new book"
            name = self.get_argument("name")
            title = self.get_argument("title")
            author = self.get_argument("author")
            if not name or not title or not author:
                return self.write({"success":False})
            if not len(name) or not len(title) or not len(author):
                return self.write({"success":False})
            print "[ NEW BOOK ] name ",name," title ",title," author ",author
            self.db.execute(
        "INSERT INTO book (name,title,author) VALUES (%s,%s,%s)",name, title,author)
            self.write({"success":True})
        except:
            self.write({"success":False})

class CategoryHandler(BaseHandler):

    def post(self):
        try:
            print "Adding new category"
            name = self.get_argument("name")
            if not name or not len(name):
                return self.write({"success":False})
            print "[ NEW CATEGORY ] name ",name
            self.db.execute(
                "INSERT INTO category (name) VALUES (%s)",name)
            self.write({"success":True})
        except:
            self.write({"success":False})

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
