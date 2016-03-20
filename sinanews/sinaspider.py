#!/usr/lib/python
#coding=utf-8

import pycurl
from io import BytesIO
import re
import json
from news_model import newsData
import mydb

class SpiderNews:
    def __init__(self):
        self.news = newsData()
        self.db = mydb.Mydb()

    def getPage(self, url):
        print url
        try:
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            page = buffer.getvalue()
            return page
#            pattern = re.compile('/{1,}([^\W]*)', re.S)
#            s = re.search(pattern, url)
#            name = s.group(1)
#            self.saveHtml(name, page)
        except Exception, e:
            print Exception, ':', e

    # def getHref(self, url):
    #     page = self.getPage(url)
    #     print "get url"
    #     pattern = re.compile('<div\s*class.*?nav-mod-1.*?>([\s\S]*?)</div>', re.S)
    #     try:
    #         gethref = re.findall(pattern, page)
    #         UrlAndName = [[]];
    #         for item in gethref:
    #             pattern = re.compile('[\s\S]*?<\s*a\s*href\s*=\s*"(.*?)".*?>(?:<\s*b\s*>|)(.*?)(?=<\s*\/b\s*>|<\s*\/a\s*>)', re.S);
    #             gethrefdetail = re.findall(pattern, item)
    #             UrlAndName.append(gethrefdetail)
    #         for item in UrlAndName:
    #             for itemdetail in item:
    #                 for itemtest in itemdetail:
    #                     print itemtest
    #         return UrlAndName
    #     except Exception, e:
    #         print Exception, ':', e
    #         return []


    def getInfo(self, url):
        # hrefs = self.getHref(url)
        hrefs = []
        hrefs.append(url)
        if(hrefs != []):
            for infourl in hrefs:
                page = ''
                if (re.search("^http", infourl)):
                    try:
                        page = self.getPage(infourl)
                    except Exception, e:
                        print Exception, ':', e
                else:
                    try:
                        page = self.getPage(("http:" + infourl))
                    except Exception, e:
                        print Exception, ':', e
                pattern = re.compile('(?:<!--\s*?LLTJ_MT:name\s*?=".+"|<meta\s*?property\s*?=\s*?"og:type"\s*?content\s*?=\s*?"article"[\s\S]*?>)')
                findname = re.search(pattern, page)
                if findname:
                    print 'It\'s a news'
                    #In sequence: keywords, description, title, url, imageurl, newsid, source, type, date
                    try:
                        pattern = re.compile('<meta\s*?name=\s*?"keywords"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['contents']['keywords'] = re.search(pattern, page).group(1).strip().decode('utf8')

                        pattern = re.compile('<meta\s*?property=\s*?"og:title"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['contents']['title'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        pattern = re.compile('<meta\s*?property=\s*?"og:url"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['url'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        pattern = re.compile('<meta\s*?property=\s*?"og:image"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['contents']['image'] = '' + re.search(pattern, page).group(1).strip().decode('utf8')
                        pattern = re.compile('<meta\s*?name=\s*?"publishid"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['id'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        pattern = re.compile('<meta\s*?name=\s*?"mediaid"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['source'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        pattern = re.compile('<\s*?div\s*?class\s*?=\s*?"site-header.*?>[\s\S]*?<\s*?div\s*?class\s*?=\s*?"bread">[\s\S]*?<a.*?">\s*?(\S*?)<\/a>')
                        self.news.data['type'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        pattern = re.compile('"time-source".*?>[\s\S]*?([0-9]{4})[^0-9]*?([0-9]{1,2})[^0-9]*?([0-9]{1,2})[^0-9]*?\s*?([0-9]{1,2}):([0-9]{1,2})[\s\S]*?<\/span>')
                        datesearch = re.search(pattern, page)
                        datestr = datesearch.group(1).strip() + datesearch.group(2).strip() + datesearch.group(3).strip() + datesearch.group(4).strip() + datesearch.group(5).strip()
                        if len(datestr) == 12:
                            self.news.data['date'] = datestr
                        else:
                            return
                        #get news abstract
                        pattern = re.compile('<meta\s*?name=\s*?"description"\s*?content\s*?=\s*?"(.*?)"')
                        if re.search(pattern, page).group(1).strip().decode('utf8') == '':
                            pattern = re.compile('<meta\s*?property=\s*?"og:description"\s*?content\s*?=\s*?"(.*?)"')
                            if re.search(pattern, page).group(1).strip().decode('utf8') == '':
                                self.news.data['contents']['abstract'] = self.news.data['contents']['title']
                            else:
                                self.news.data['contents']['abstract'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        else:
                            self.news.data['contents']['abstract'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        #get news content
                        pattern = re.compile('<\s*?div\s*class\s*?=\s*?"article\s*?article_16(?:[^>]*?)>[\s\S]*?(?:<div(?:[^>]*?>[\s\S]*?<\/div>))*([\s\S]*?<\/p>[\s\S]*?)<\/div>')
                        pagecontent = re.search(pattern, page).group(1).strip()
                        pattern = re.compile('<\s*?div\s*?class\s*?=\s*?"img_wrapper"(?:[^<])*?<img.*?src\s*?=\s*?"(.*?)"[\s\S]*?<\/div>')
                        detailimage = re.findall(pattern, pagecontent)
                        image = self.news.data['contents']['image']
                        for item in detailimage:
                            try:
                                if item.strip() in image:
                                    pass
                                else:
                                    image += '~@~' + item.strip()
                            except Exception, e:
                                print Exception, ':', e
                        self.news.data['contents']['image'] = image
                        pattern = re.compile('<p(?:\s*?style(?:[^>]*)?|)>([\s\S]*?)</p>')
                        detailcontent = re.findall(pattern, pagecontent)
                        content = ''
                        for item in detailcontent:
                            content += item
                        pattern = re.compile('<\s*(\S+)(\s*?[^>]*)?>')
                        content = re.sub(pattern, '',content)
                        pattern = re.compile('<\s*?\/.*?>')
                        content = re.sub(pattern, '',content)
                        pattern = re.compile('&nbsp;')
                        content = re.sub(pattern, ' ',content)
                        self.news.data['contents']['context'] = content.decode('utf8')
                        print 'id:' + '\n' + self.news.data['id']
                        print 'source:' + '\n' + self.news.data['source']
                        print 'date:' + '\n' + self.news.data['date']
                        print 'type:' + '\n' + self.news.data['type']
                        print 'url:' + '\n' + self.news.data['url']
                        print 'title:' + '\n' + self.news.data['contents']['title']
                        print 'context:' + '\n' + self.news.data['contents']['context']
                        print 'keywords:' + '\n' + self.news.data['contents']['keywords']
                        print 'abstract:' + '\n' + self.news.data['contents']['abstract']
                        print 'image:' + '\n' + self.news.data['contents']['image']
                        # self.db.insert_news(self.news)
                        # print 'insert successful'
                        #analysis by json
                        # encodedjson = json.dumps(self.news.data)
                        # decodedjson = json.loads(encodedjson)
                        # for item in decodedjson.keys():
                        #     if type(decodedjson[item]) == dict:
                        #         for a in decodedjson[item].keys():
                        #                 print a + ':'
                        #                 print decodedjson[item][a]
                        #     else:
                        #         print item + ':'
                        #         print decodedjson[item]
                    except Exception, e:
                        print Exception, ':', e
                        return
                else:
                    print 'not a news'

    def show_info(self):
        news = self.db.query_news()
        # for item in news:
        #     for i in range(0 , len(item) - 1):
        #         print item[i]
        for item in news:
            encodedjson = json.dumps(item)
            decodedjson = json.loads(encodedjson)
            for item in decodedjson.keys():
                if type(decodedjson[item]) == dict:
                    for a in decodedjson[item].keys():
                        print a + ':'
                        print decodedjson[item][a]
                else:
                    print item + ':'
                    print decodedjson[item]


if __name__ == '__main__':
    siteURL = 'http://news.sina.com.cn/w/2015-10-07/doc-ifxiqtqy0405427.shtml'
    spider = SpiderNews()
    spider.getInfo(siteURL)
    # spider.show_info()