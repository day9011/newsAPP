__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

import MySQLdb
from news_model import newsData

#news model class
class Mydb:
    def __init__(self):
        self.username = 'day9011'
        self.password = '123456'
        self.db = 'news_database'
        self.port = 3306
        self.host = 'localhost'
        self.charset = 'utf8'
        self.conn = ''

    def connect_db(self):
        try:
            print "start connect"
            self.conn = MySQLdb.connect(host = self.host, user = self.username, passwd = self.password, db = self.db, port = self.port, read_default_file='/etc/my.cnf', charset = self.charset)
            print "connect database successfully"
        except Exception, e:
            self.conn = ''
            print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    def insert_news(self, news):
        print "insert beginning"
        self.connect_db()
        sql_if_exist_id = 'SELECT * FROM news_attribute WHERE news_id = "%s"' % (news.data['id'])
        cur = self.conn.cursor()
        try:
            cur.execute(sql_if_exist_id)
            results = cur.fetchall()
            cur.close()
            if results == ():
                pass
            else:
                print "It's exist'"
                return
        except Exception, e:
            print Exception, ':', e
            return
        sql_attribute = 'INSERT IGNORE INTO news_attribute VALUES(%s, %s, %s, %s)'
        insert_attribute = [news.data['id'], news.data['url'], news.data['date'], news.data['source']]
        sql_contents = 'INSERT IGNORE INTO news_contents VALUES(%s, %s, %s, %s, %s, %s)'
        insert_contents = [news.data['id'], news.data['contents']['title'], news.data['contents']['context'], news.data['contents']['abstract'], news.data['contents']['keywords'], news.data['contents']['image']]
        try:
            cur = self.conn.cursor()
            cur.execute(sql_attribute, insert_attribute)
            cur.execute(sql_contents, insert_contents)
            self.conn.commit()
            cur.close()
            self.disconnect_db()
            print "insert successfully id:" + news.data['id']
        except Exception, e:
            self.conn = ''
            print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    def query_news(self, *args):
        def query_news1(self, sqlstr, num):
            self.connect_db()
            cur = self.conn.cursor()
            cur.execute(sqlstr)
            results = cur.fetchmany(num)
            cur.close()
            self.disconnect_db()
            return results
        #get top number of news
        def query_news2(self, num):
            self.connect_db()
            cur = self.conn.cursor()
            sqlstr = 'SELECT DISTINCT * FROM news_attribute, news_contents WHERE news_attribute.news_id = news_contents.news_id ORDER BY news_attribute.news_date LIMIT ' + '%d' % num
            try:
                cur.execute(sqlstr)
                results = cur.fetchall()
                cur.close()
                self.disconnect_db()
                newsresults = []
                for item in results:
                    newsitem = newsData().data
                    newsitem['id'] = item[0]
                    newsitem['url'] = item[1]
                    newsitem['date'] = item[2]
                    newsitem['source'] = item[3]
                    newsitem['contents']['title'] = item[4]
                    newsitem['contents']['context'] = item[5]
                    newsitem['contents']['abstract'] = item[6]
                    newsitem['contents']['keywords'] = item[7]
                    newsitem['contents']['image'] = item[8]
                    newsresults.append(newsitem)
                return newsresults
            except Exception, e:
                cur.close()
                self.disconnect_db()
                print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
        def query_news3(self):
            self.connect_db()
            cur = self.conn.cursor()
            sqlstr = 'SELECT DISTINCT * FROM news_attribute, news_contents WHERE news_attribute.news_id = news_contents.news_id'
            try:
                cur.execute(sqlstr)
                results = cur.fetchall()
                cur.close()
                self.disconnect_db()
                # return results
                newsresults = []
                for item in results:
                    newsitem = newsData().data
                    newsitem['id'] = item[0]
                    newsitem['url'] = item[1]
                    newsitem['date'] = item[2]
                    newsitem['source'] = item[3]
                    newsitem['contents']['title'] = item[5]
                    newsitem['contents']['context'] = item[6]
                    newsitem['contents']['abstract'] = item[7]
                    newsitem['contents']['keywords'] = item[8]
                    newsitem['contents']['image'] = item[9]
                    newsresults.append(newsitem)
                return newsresults
            except Exception, e:
                cur.close()
                self.disconnect_db()
                print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
        if len(args) == 2:
            print "It's in 1"
            return query_news1(self, *args)
        elif len(args) == 1:
            print "It's in 2"
            return query_news2(self, *args)
        else:
            print "It's in 3"
            return query_news3(self, *args)

    def disconnect_db(self):
        if self.conn != '':
            self.conn.close()
            self.conn = ''
