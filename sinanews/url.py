__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from api import *

url = [
    (r"/news-abstract", news_abstract),
    (r"/news-num", news_num),
    (r"/login", user.login),
    (r"/register", user.register)
]
