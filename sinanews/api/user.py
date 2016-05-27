#!/usr/bin/env python2.7
# Name: user
# Function: user auth
# Date: 2016-05-27
# Email: day9011@gmail.com
__author__ = 'day9011'

from tornado.web import RequestHandler
import tornado
from utils.news_log import getlogger
import json
from lib.db import Mydb
from utils.post_valid import *

logger = getlogger()
__all__ = ['login', 'register']

class login(RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        ret = ''
        db = Mydb()
        try:
            body = self.request.body_arguments
            Args = [
                self_argument('username', True, helpinfo='Miss username'),
                self_argument('password', True, helpinfo='Miss password'),
            ]
            s, vals = DataIsValid(Args, body)
            if s:
                raise Exception(vals)
            username = vals['username']
            password = vals['password']
            if not (username or password):
                raise Exception('no password or username')
            sql = "SELECT * FROM user WHERE username='%s' and password='%s'" % (username, password)
            s, f = db.get(sql)
            if s or not(f):
                raise Exception("No user")
            else:
                ret = json.dumps({'status': s, 'content': 'OK'})
        except Exception, e:
            logger.error(str(e))
            ret = json.dumps({'status': '-110', 'content': str(e)})
        finally:
            self.write(ret)
            self.finish()

class register(RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        ret = ''
        db = Mydb()
        try:
            body = self.request.body_arguments
            Args = [
                self_argument('username', True, helpinfo='Miss username'),
                self_argument('password', True, helpinfo='Miss password'),
            ]
            s, vals = DataIsValid(Args, body)
            if s:
                raise Exception(vals)
            username = vals['username']
            password = vals['password']
            if not (username or password):
                raise Exception('no password or username')
            sql = "SELECT * FROM user WHERE username='%s' and password='%s'" % (username, password)
            s, f = db.get(sql)
            if f:
                raise Exception("The user is exist!")
            else:
                sql = "INSERT INTO user VALUES (%s, %s)"
                s, f = db.modify(sql, [username, password])
                if s:
                    raise Exception(f)
                ret = json.dumps({'status': 0, 'content': 'OK'})
        except Exception, e:
            logger.error(str(e))
            ret = json.dumps({'status': '-110', 'content': str(e)})
        finally:
            self.write(ret)
            self.finish()