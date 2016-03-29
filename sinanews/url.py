__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from news_abstract import news_abstract

url = [
    (r"/news-abstract", news_abstract),
]
