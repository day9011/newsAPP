#!/usr/lib/python
#coding=utf-8
__author__ = 'dinghanyu'

from tornado.web import RequestHandler
import tornado

APP_KEY = '470165278'
APP_SECRET = '6196610a36ea83125320b163d490a441'
CALLBACK_URL = 'http://121.42.145.214/weibo'

class weibo(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        #code = self.request.get('code')
        #client = APIClient(app_key = APP_KEY, app_secret = APP_SECRET, redirect_uri = CALLBACK_URL)
        #r = client.request_access_toke(code)
        #access_token = r.access_token
        #expires_in = r.expires_in
        #client.set_access_token(access_token, expires_in)
        #print client.statuses.user_timeline.get()
        print "someone visited"
        self.write("test for weibo app")
        self.finish()
