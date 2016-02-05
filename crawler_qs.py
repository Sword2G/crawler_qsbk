# -*- coding:utf-8 -*-
import requests
import re
import bs4
import codecs
import sqlite3
from bs4 import BeautifulSoup
import time
import codecs
import Config
import os

COUNTS = 0

class QSCrawlerUtils(object):
    @staticmethod
    def striprn(text):
        text = text.strip()
        i = 0
        for char in text:
            if char == '\n':
                i += 1
            else:
                break
        text = text[i:]
        j = i
        for char in text:
            if char != '\n':
                j += 1
        text = text[0:j]
        return text

class QSCrawlerMain(object):
    def __init__(self,config):
        self.config = config
        self.qs_header = {
        'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        }

    def gethtml(self, url):
        try:
            r = requests.get(url, headers = self.qs_header)
            html = r.text
            return html
        except requests.HTTPError,e:
            print e

    def getqsfromhtml(self, html):    
        soup = BeautifulSoup(html,'html.parser')
        QSS = soup.find_all('div',class_='article block untagged mb15')

        for qsitem in QSS:
            if type(qsitem) == bs4.element.Tag:
                author = qsitem.find('div',class_='author clearfix')
                if type(author) == bs4.element.Tag:
                     author = author.get_text()
                     author = QSCrawlerUtils.striprn(author)
                            
                qscontent = qsitem.find('div',class_='content')
                qscontent =  qscontent.get_text()
                qscontent = QSCrawlerUtils.striprn(qscontent)

                likenums_and_commentnums = qsitem.find_all('i',class_ = 'number')
    ##            print likenums_and_commentnums
                if len(likenums_and_commentnums) != 2:
                    likeNums = 0
                    commentbums = 0
                else:                
                    likeNums = likenums_and_commentnums[0].get_text()
                    commentbums = likenums_and_commentnums[1].get_text()
    ##            counts += 1
                global COUNTS
                COUNTS += 1
                print str(COUNTS) + ' has found>>>>>>>>'
                print 'start to store into database'
                #warning: keyword 'self' is needed
                self.insert2DB((COUNTS,author,qscontent,likeNums, commentbums,time.time()))

    def createtable(self):
        conn= sqlite3.connect(self.config.db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE QSS(
                       ID INT  PRIMARY KEY NOT NULL,
                       AUTHOR TEXT,
                       QSCONTENT TEXT,
                       PRAISE INT,
                       COMMENTS INT,
                       pp CHAR(10));              
                       ''')
        conn.commit()
        conn.close()
    
    def insert2DB(self, eachqs):
        conn= sqlite3.connect(self.config.db_file)
        cursor = conn.cursor()
        cursor.execute('insert into QSS values(?,?,?,?,?,?)',eachqs)
        conn.commit()
        conn.close()

    def showqs(self):
        print '123'
        conn= sqlite3.connect(self.config.db_file)
        cursor = conn.cursor()
        cursor.execute('select * from QSS')
        for row in cursor.fetchall():      
            print "ID = ", row[0]
            print "AUTHOR = ", row[1]
            print "QSCONTENT = ", row[2]
            print "PRAISE = ", row[3]
            print "COMMENTS = ", row[4]  
        
        conn.commit()
        conn.close()

    def generateHtml(self):
        conn= sqlite3.connect(self.config.db_file)
        cursor = conn.cursor()
        cursor.execute('select * from QSS')
        values = cursor.fetchall()
        
        result = codecs.open(self.config.result_file, 'w', 'utf-8')
               
        result.writelines('<html><head>\n')
        result.writelines('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
        result.writelines('<title>Rent Crawer Result</title></head><body>\n')
        result.writelines('<table rules=all>\n')
        result.writelines('<h1>''</h1>\n')
        result.writelines('<tr><td>Index</td><td>Author</td><td>Content</td><td>Likenums</td><td>Comments</td><td>Timestamp</td></tr>\n')

    ##    result.writelines('<tr><td>序号Index</td><td>作者Author</td><td>内容Content</td><td>赞人数Likenums</td><td>评论人数Comments</td><td>时间戳Timestamp</td></tr>')
        for row in values:
            result.write('<tr>')
            for member in row:
                result.write('<td>')
                if isinstance(member,int):
                    member = str(member)
                    result.write(member)
                elif isinstance(member,unicode):
                    result.write(member)
                result.write('</td>')
            result.write('</tr>')
            
        result.writelines('</table>\n')
        result.writelines('</body></html>\n')

        result.flush()
        result.close()

    def run(self):
        print 'start QSCrawlerMain '
        page = 1

        #self is needed
        self.createtable()
         
        print 'Start crawler>>>>>>>'
        #warning : the type of variable read from config.ini is str
        while page < int(self.config.page_nums):#
            url = 'http://www.qiushibaike.com/8hr/' + str(page) + '/3/?s=4845092'        
            html = self.gethtml(url)          
            self.getqsfromhtml(html)                  
            page += 1
            
        self.generateHtml()
        print '>'*18
        print "Crawler Finished,Please open result.html to view result"
        
class QSCrawler(object):
    def __init__(self):
        this_file_dir = os.path.split(os.path.realpath(__file__))[0]
        config_file_path = os.path.join(this_file_dir, 'config.ini')
        self.config = Config.Config(config_file_path)

    def run(self):
        qscrawlermain = QSCrawlerMain(self.config)
        qscrawlermain.run()      


# Main entry
if __name__ == '__main__':
    print 'start'
##    # set encoding
##    reload(sys)
##    sys.setdefaultencoding('utf8')
    prog_info = "QiuShiBaiKe Crawler 1.2\nBy Licong\nhttp://my.oschina.net/v5871314\n"
    print prog_info

    qscrawler = QSCrawler()
    qscrawler.run()


   
    
   
