# -*- coding:utf-8 -*-

'''
    项目名称：电影爬虫v0.1
    项目目标：爬取电影天堂上的电影名称与对应的迅雷下载链接
'''


import re
import urllib
import urllib2
import time
import sys




class MovieSpider(object):

    def __init__(self,url):
        self.URL = url
        self.user = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36'}

    def PageResponse(self,url):
        request = urllib2.Request(url,headers = self.user)
        response = urllib2.urlopen(request)
        html = response.read().decode('gbk')
        return html

    def FirstPage(self):
        '''
        匹配首页的电影链接
        :param URL:
        :return:
        '''
        html = self.PageResponse(self.URL)
        movieField = re.findall("<a href='(.*?)'>",html)  #将网页中表示电影链接的区域划分出来
        # movieLink = re.findall("<a href='(.*?)'>",movieField,re.S)
        i = 0
        for l in movieField:
            link = self.URL + l
            i += 1
            print '第%s部爬取完成'%i
            if i < 170:
                yield link
            else:
                raise StopIteration

    def SecondPage(self,link):
        '''
        获取网页上的电影的名称和电影对应的迅雷链接
        :param link:
        :return:
        '''
        text = 'movielist.txt'
        for l in link:
            html = self.PageResponse(l)
            movieName = re.findall(u'<div class="title_all"><h1><font color=#07519a>(.*?)</font></h1></div>',html,re.S)
            movieDownload = re.findall(u'bgcolor="#fdfddf"><a href="(.*?)">',html,re.S)
            with open(text,'ab') as handles:
                handles.write('电影名：%s\n迅雷下载链接：%s\n网页原链接：%s\n\n'%(movieName[0].encode('utf-8'),movieDownload[0].encode('utf-8'),l.encode('utf-8')))

            print '%s信息获取完成！'%movieName[0].encode('utf-8')
    def mian(self):
        self.SecondPage(self.FirstPage())

if __name__ == '__main__':
    print ('''
    电影网络爬虫：爬取电影天堂上最新的电影
    .....
    ''')

    try:
        spider = MovieSpider('http://www.dytt8.net/')
        spider.mian()
    except:
        print "Unexpected error:", sys.exc_info() # sys.exc_info()返回出错信息
        raw_input('press enter key to exit') #这儿放一个等待输入是为了不让程序退出







