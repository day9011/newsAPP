__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from news_abstract import news_abstract
from news_num import news_num

url = [
    (r"/news-abstract", news_abstract),
    (r"/news-num", news_num),
]
