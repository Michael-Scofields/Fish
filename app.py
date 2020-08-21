# python app.py -port=8000 -log_file_prefix=logs/app_log_8000.log
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import os
import time

define("port", default=8000, help="Run server on a specific port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def _request_summary(self):
        return "%s %s (%s) %s\n" % (self.request.method, self.request.uri, self.request.remote_ip, self.request.headers["User-Agent"],)


class IntroduceHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('introduce.html')


class PostHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('post.html')


class MainHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')

    def post(self, *args, **kwargs):
        stime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # name = self.get_argument('name', None)
        phonenu = self.get_argument('phone', None)
        # if name == "" and phonenu == "":
        if phonenu == "":
            self.render('post.html')
        else:
            ip = self.request.remote_ip
            Agent = self.request.headers["User-Agent"]
            # collect_info = "{} -> [{}]-{}-{} -> {}\n".format(stime, ip, name, phonenu, Agent)
            collect_info = "{} -> [{}]-{} -> {}\n".format(stime, ip, phonenu, Agent)
            print (collect_info)
            with open("logs/collect.txt", 'a+') as file:
                file.write(collect_info)
            self.render('index.html')


settings = {"debug": False, "static_path": os.path.join(os.path.dirname(__file__), 'static')}
application = tornado.web.Application(
    [
        (r"/introduce", IntroduceHandler),
        (r"/index", MainHandler),
        (r"/.*", PostHandler),
    ], **settings)


if __name__ == "__main__":
    print ("Collecting...")
    http_server = tornado.httpserver.HTTPServer(application)
    tornado.options.parse_command_line()
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
