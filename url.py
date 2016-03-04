__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from weibo import weibo
from testapp import testapp


url = [
    (r"/weibo", weibo),
    (r'/app', testapp),
]
