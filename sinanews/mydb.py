__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8

import MySQLdb
from news_model import *
from writeToLog import *
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
        self.logstr = ''

    def connect_db(self):
        try:
            self.logstr += "start connect\n"
            self.conn = MySQLdb.connect(host = self.host, user = self.username, passwd = self.password, db = self.db, port = self.port, read_default_file='/etc/my.cnf', charset = self.charset)
            self.logstr += "connect database successfully\n"
        except Exception, e:
            self.conn = ''
            error_log(e.__class__.__doc__)
            return

    def insert_news(self, news):
        self.logstr += "insert beginning\n"
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
                self.logstr += "It's exist\n"
                error_log(self.logstr)
                self.logstr = ""
                return
        except Exception, e:
            error_log(e.__class__.__doc__)
            return
        sql_str = 'INSERT INTO news_detail VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        insert_info = [news.data['id'], news.data['url'], news.data['date'], news.data['source'], news.data['title'], news.data['content'], news.data['abstract'], news.data['keywords'], news.data['image']]
        try:
            cur = self.conn.cursor()
            cur.execute(sql_str, insert_info)
            self.conn.commit()
            cur.close()
            self.disconnect_db()
            self.logstr += "insert successfully id:" + news.data['id'] + "\n"
            normal_log(self.logstr)
            self.logstr = ""
        except Exception, e:
            self.conn = ''
            error_log(e.__class__.__doc__)

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
                self.logstr += "query successful\n"
                normal_log(self.logstr)
                self.logstr = ""
                return results
            except Exception, e:
                error_log(e.__class__.__doc__)
                return
        def query_news2(self):
            self.connect_db()
            cur = self.conn.cursor()
            sqlstr = 'SELECT * FROM news_detail ORDER BY news_cursor desc'
            try:
                cur.execute(sqlstr)
                results = cur.fetchall()
                cur.close()
                self.disconnect_db()
                # return results
                newsresults = handle_query_result(results)
                self.logstr += "query successful\n"
                normal_log(self.logstr)
                self.logstr = ""
                return newsresults
            except Exception, e:
                cur.close()
                self.disconnect_db()
                error_log(e.__class__.__doc__)
        #print "start query"
        if len(args) > 0:
            #print "It's in 1"
            return query_news1(self, *args)
        else:
            #print "It's in 2"
            return query_news2(self)

    def disconnect_db(self):
        if self.conn != '':
            self.conn.close()
            self.conn = ''

#db = Mydb()
#result = db.query_news('select * from news_detail where news_cursor > 5 order by news_cursor')
#print result
