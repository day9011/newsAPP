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
import socket

setting = {
    'static_path' : os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application(
    handlers = url,
    # autoreload = True,
    # debug = True,
    **setting
)

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
    # sockets = tornado.netutil.bind_sockets(8888)
    # tornado.process.fork_processes(0)
    # server = tornado.httpserver.HTTPServer(application)
    # server.add_sockets(sockets)
    # tornado.ioloop.IOLoop.current().start()

