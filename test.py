#!/usr/bin/env python2.7
#coding=utf-8
def deco(text):
    def describe(func):
        def _deco():
            print("before myfunc() called.")
            func()
            print("  after myfunc() called.")
            print "text:", text
        return _deco
    return describe

@deco("test")
def myfunc():
    print(" myfunc() called.")

def fc():
    print "func() called"

print myfunc.__name__
fc = deco("func")(fc)
print fc.__name__
myfunc()
fc()

class test(object):
    def __init__(self,a=None, b=None, c=None):
        pass
    def pr(self, *args, **kwargs):
        for item in args:
            print item
    a = 1
    b = 2
    c = 3
    pr(a, b, c)
a = test()
# def deco(func):
#     def _deco():
#         print("before myfunc() called.")
#         func()
#         print("  after myfunc() called.")
#         # 不需要返回func，实际上应返回原函数的返回值
#     return _deco
#
# @deco
# def myfunc():
#     print(" myfunc() called.")
#     return 'ok'
#
# myfunc()
# myfunc()