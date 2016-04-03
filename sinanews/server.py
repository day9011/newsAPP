__author__ = 'dinghanyu'
#!/usr/bin/python
#coding=utf-8


from url import url
import os
import tornado.web
import tornado.process
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.log
import socket
from tornado.options import define, options
import sys


define("port", default = 8888, help="run on specific port", type=int)

setting = {
    'static_path' : os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret' : "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    'xsrf_cookies' : True,
    #'autoreload' : True,
    #'debug' : False,
}

application = tornado.web.Application(
    handlers = url,
    # debug = True,
    **setting
)

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    args = sys.argv
    args.append('--log_file_prefix=/var/log/news/server.log')
    tornado.options.parse_command_line()
    server.bind(options.port)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
    # sockets = tornado.netutil.bind_sockets(8888)
    # tornado.process.fork_processes(0)
    # server = tornado.httpserver.HTTPServer(application)
    # server.add_sockets(sockets)
    # tornado.ioloop.IOLoop.current().start()

