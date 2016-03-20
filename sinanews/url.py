__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from MainHandler import MainHandler


url = [
    (r"/", MainHandler),
]