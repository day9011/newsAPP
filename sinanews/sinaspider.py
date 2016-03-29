#!/usr/lib/python
#coding=utf-8

import pycurl
from io import BytesIO
import re
import json
from news_model import newsData
import mydb
import time

class SpiderNews:
    def __init__(self, url):
        self.news = newsData()
        self.db = mydb.Mydb()
        self.url = url

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


    def getInfo(self, hrefs):
        # hrefs = self.getHref(url)
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
                        self.news.data['keywords'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        pattern = re.compile('<meta\s*?property=\s*?"og:title"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['title'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        self.news.data['url'] = infourl
                        pattern = re.compile('<meta\s*?property=\s*?"og:image"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['image'] = '' + re.search(pattern, page).group(1).strip().decode('utf8')
                        pattern = re.compile('<meta\s*?name=\s*?"publishid"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['id'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        pattern = re.compile('<meta\s*?name=\s*?"mediaid"\s*?content\s*?=\s*?"(.*?)"')
                        self.news.data['source'] = re.search(pattern, page).group(1).strip().decode('utf8')
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
                                self.news.data['abstract'] = self.news.data['title']
                            else:
                                self.news.data['abstract'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        else:
                            self.news.data['abstract'] = re.search(pattern, page).group(1).strip().decode('utf8')
                        self.news.data['abstract'] = self.news.data['abstract'].split('。')[0] + '。'
                        #get news content
                        # print "get content"
                        pattern = re.compile('<\s*?div\s*class\s*?=\s*?"content"(?:[^>]*?)>[\s\S]*?(?:<div(?:[^>]*?>[\s\S]*?<\/div>))*([\s\S]*?<\/p>[\s\S]*?)<\/div>')
                        pagecontent = re.search(pattern, page).group(1).strip()
                        self.news.data['content'] = pagecontent.decode('utf8')
                        self.news.data['content'] = '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>\n' + self.news.data['content'] + '</div>\n</body></html>'
#                        print 'id:' + '\n' + self.news.data['id']
#                        print 'source:' + '\n' + self.news.data['source']
#                        print 'date:' + '\n' + self.news.data['date']
#                        print 'url:' + '\n' + self.news.data['url']
#                        print 'title:' + '\n' + self.news.data['title']
#                        print 'content:' + '\n' + self.news.data['content']
#                        print 'keywords:' + '\n' + self.news.data['keywords']
#                        print 'abstract:' + '\n' + self.news.data['abstract']
#                        print 'image:' + '\n' + self.news.data['image']
                        self.db.insert_news(self.news)
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


    def getHref(self):
        pagefirst = ""
        valued_hrefs = []
        c_time = self.get_time()
#        c_time = '2016-03-28'
        for url in self.url:
            try:
                pagefirst = self.getPage(url).decode(('utf8'))
            except:
                try:
                    pagefirst = self.getPage(url).decode(('gbk'))
                except Exception, e:
                    print e
            pattern = re.compile('<a\s*?href\s*?=\s*?"(http[\s\S]*?)"[^>]*?>')
            hrefs = re.findall(pattern, pagefirst)
            # pattern = re.compile('(?i)t\s*?f\s*?b\s*?o\s*?y\s*?|易\s烊\s*?千\s*?玺|王\s*?源|王\s*?俊\s*?凯')
            # test = re.findall(pattern, pagefirst)
            # print test
            # i = 1
            # for item in hrefs:
            #     print "href" + str(i) + ":" + item[0] + " url:" + item[1]
            #     i += 1
            for item in hrefs:
                pattern = re.compile('http://ent[\s\S]*?/([0-9]{4}-[0-9]{2}-[0-9]{2})/doc')
                try:
                    if re.search(pattern, item).group(1) == c_time:
                        if item in valued_hrefs:
                            continue
                        else:
                            valued_hrefs.append(item)
                        re.search(pattern, item).group(1)
#                    if item in valued_hrefs:
#                        continue
#                    else:
#                        valued_hrefs.append(item)
                except:
                    pass
        self.getInfo(valued_hrefs)

    def get_time(self):
        current_time = time.strftime("%Y-%m-%d", time.localtime())
        return current_time

if __name__ == '__main__':
    siteURL = ['http://search.sina.com.cn/?q=%D2%D7%EC%C8%C7%A7%E7%F4&range=all&c=news&sort=time'
               ,'http://search.sina.com.cn/?q=tfboys&range=all&c=news&sort=time'
               ,'http://search.sina.com.cn/?q=%CD%F5%D4%B4&range=all&c=news&sort=time'
               ,'http://search.sina.com.cn/?q=%CD%F5%BF%A1%BF%AD&range=all&c=news&sort=time']
    spider = SpiderNews(siteURL)
    spider.getHref()
#    spider.getInfo(['http://ent.sina.com.cn/v/m/2016-03-19/doc-ifxqnskh1027006.shtml'])
    # spider.show_info()
