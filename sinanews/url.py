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
    (r"/register", user.register),
    (r"/topic-post", topic.post_topic),
    (r"/topic/list", topic.get_topic_list),
    (r"/topic/detail/(.*)", topic.get_topic),
    (r"/comment-post", comment.post_comment),
    (r"/comments/id/(.*)", comment.get_comments),
    (r"/comment/page/(.*)", comment.get_comments_page)
]
