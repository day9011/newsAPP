__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

import MySQLdb
from news_model import newsData

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
        sql_if_exist_id = 'SELECT * FROM news_detail WHERE news_id = "%s"' % (news.data['id'])
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
        sql_str = 'INSERT INTO news_detail VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        insert_info = [news.data['id'], news.data['url'], news.data['date'], news.data['source'], news.data['title'], news.data['content'], news.data['abstract'], news.data['keywords'], news.data['image']]
        try:
            cur = self.conn.cursor()
            cur.execute(sql_str, insert_info)
            self.conn.commit()
            cur.close()
            self.disconnect_db()
            print "insert successfully id:" + news.data['id']
        except Exception, e:
            self.conn = ''
            print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    def query_news(self, *args):
        def query_news1(self, sqlstr, num = 0):
            try:
                if num == 0:
                    self.connect_db()
                    cur = self.conn.cursor()
                    cur.execute(sqlstr)
                    results = cur.fetchall()
                    cur.close()
                    self.disconnect_db()
                else:
                    self.connect_db()
                    cur = self.conn.cursor()
                    cur.execute(sqlstr)
                    results = cur.fetchmany(num)
                    cur.close()
                    self.disconnect_db()
                print "query successful"
                return results
            except Exception, e:
                print Exception, ':', e
                return
        def query_news2(self):
            self.connect_db()
            cur = self.conn.cursor()
            sqlstr = 'SELECT * FROM news_detail'
            try:
                cur.execute(sqlstr)
                results = cur.fetchall()
                cur.close()
                self.disconnect_db()
                # return results
                newsresults = []
                for item in results:
                    newsitem = newsData().data
                    newsitem['cursor'] = item[0]
                    newsitem['id'] = item[1]
                    newsitem['url'] = item[2]
                    newsitem['date'] = item[3]
                    newsitem['source'] = item[4]
                    newsitem['title'] = item[5]
#                    newsitem['content'] = item[6]
                    newsitem['content'] = ""
                    newsitem['abstract'] = item[7]
                    newsitem['keywords'] = item[8]
                    newsitem['image'] = item[9]
                    newsresults.append(newsitem)
                print "query successful"""
                return newsresults
            except Exception, e:
                cur.close()
                self.disconnect_db()
                print Exception, ':', e
        print "start query"
        if len(args) > 0:
            print "It's in 1"
            return query_news1(self, *args)
        else:
            print "It's in 2"
            return query_news2(self)

    def disconnect_db(self):
        if self.conn != '':
            self.conn.close()
            self.conn = ''

#db = Mydb()
#result = db.query_news('select * from news_detail', 1)
#print result
