# -*- coding: utf-8 -*-
import re
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
from lxml import etree

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dianping
collection = db.classification  # 类别表

#import redis

#r = redis.Redis(host='127.0.0.1', port=6379, db=0)

ii = 0


def secClassFind(selector, classid):
    global ii
    ii += 1
    secItems = selector.xpath('//div[@class="sec-items"]/a')
    for secItem in secItems:
        url = secItem.get('href')
        title = secItem.text
        classid = collection.insert({'classname': title, 'pid': classid})
        classurl = '%s,%s,%i,%s' % (classid, url, ii, title)
        r.lpush('classurl', classurl)


def findRootNode(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req_timeout = 5
    req = Request(url=url, headers=headers)
    f = urlopen(req, None, req_timeout)
    s = f.read()
    s = s.decode("utf-8")
    # beautiful 提取数据
    soup = BeautifulSoup(s, 'html.parser')
    links = soup.find_all(name='li', class_="first-item")
    for link in links:
        selector = etree.HTML(str(link))
        '''
        indexTitleUrls = selector.xpath('//a[@class="index-title"]/@href')
        #获取一级类别url和title
        for titleurl in indexTitleUrls:
            print(titleurl)
        '''
        indexTitles = selector.xpath('//a[@class="index-title"]/text()')
        for title in indexTitles:
            print(title)
            classid = collection.insert({'classname': title, 'pid': None})
            # 第二级别url
            secClassFind(selector, classid)
            # print(rs)
            print('-------------')

        print('----------------------------------------------')


findRootNode('https://www.dianping.com/nanjing/ch0')