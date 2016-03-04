#!/usr/bin/env python2.7

from tornado.web import RequestHandler
import tornado

class testapp(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('app.html')

