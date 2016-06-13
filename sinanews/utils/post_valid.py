#!/usr/bin/env python2.7
# Name: post_valid
# Function: legitimacy judgement about post data
# Date: 2016-05-27
# Email: day9011@gmail.com
__author__ = 'day9011'

__all__ = ['DataIsValid', 'self_argument']
import re

def DataIsValid(Args, body):
    ret = {}
    try:
        for item in Args:
            if item['required']:
                if item['key'] == "password" or item['key'] == "username" :
                    if re.search(r'[^0-9a-z@_.-]', body[item['key']][0]):
                        return -22, "It's illegal letter in this item"
                elif item['key'] not in body:
                    return -21, item['helpinfo']
            ret[item['key']] = body[item['key']][0]
        return 0, ret
    except Exception, e:
        return -120, str(e)

def self_argument(key, required=False, default='', helpinfo=''):
    arg = {
        'key': key,
        'required': required,
        'default': default,
        'helpinfo': helpinfo
    }
    return arg