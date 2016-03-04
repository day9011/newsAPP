__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

from weibo import APIClient

APP_KEY = '470165278'
APP_SECRET = '6196610a36ea83125320b163d490a441'
CALLBACK_URL = 'http://121.42.145.214/weibo'

client = APIClient(app_key = APP_KEY, app_secret = APP_SECRET, redirect_uri = CALLBACK_URL)
url = client.get_authorize_url()

