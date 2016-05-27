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
    for item in Args:
        if item['required']:
            if item['key'] in body:
                if re.search(r'[^0-9a-z@_.-]', body[item['key']][0]):
                    return -22, "It's illegal letter in this item"
                ret[item['key']] = body[item['key']][0]
            else:
                return -21, item['helpinfo']
    return 0, ret

def self_argument(key, required=False, default='', helpinfo=''):
    arg = {
        'key': key,
        'required': required,
        'default': default,
        'helpinfo': helpinfo
    }
    return arg