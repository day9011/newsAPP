__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

class newsData:
    def __init__(self):
        self.data = {
            "id" : "",
            "source" : "",
            "date" : "",
            "type" : "",
            "url" : "",
            "contents" : {
                "title" : "",
                "context" : "",
                "keywords" : "",
                "abstract" : "",
                "image" : "",
            }
        }
