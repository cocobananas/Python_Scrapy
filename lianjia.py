# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:15:00 2018

@author:
"""

import urllib
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup
from urllib import request

headers = {
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
}
url_l = 'https://bj.lianjia.com/zufang/pg'

ser1 = pd.Series([], name='房屋ID')
ser2 = pd.Series([], name='标题')
ser3 = pd.Series([], name='小区')
ser4 = pd.Series([], name='户型')
ser5 = pd.Series([], name='面积')
ser6 = pd.Series([], name='朝向')
ser7 = pd.Series([], name='区域')
ser8 = pd.Series([], name='楼层高度')
ser9 = pd.Series([], name='建成时间')
ser10 = pd.Series([], name='楼层结构')
ser11 = pd.Series([], name='月租金')

index = 0

for i in range(1, 101):
    url = url_l + str(i)
    req = request.Request(url)
    res = request.urlopen(req)
    html = res.read()
    soup = BeautifulSoup(html, 'lxml')
    houselist = soup.find('ul', id='house-lst').contents
    for house in houselist:
        ser1[index] = house['data-id']
        houseinfo = house.find('div', class_='info-panel')
        ser2[index] = houseinfo.h2.a['title']
        regioninfo = houseinfo.find('div', class_='where')
        regionlist = [i for i in regioninfo.stripped_strings]
        ser3[index] = regionlist[0]
        ser4[index] = regionlist[1]
        ser5[index] = regionlist[2]
        ser6[index] = regionlist[3]
        otherinfo = houseinfo.find('div', class_='con')
        otherlist = [i for i in otherinfo.stripped_strings]
        ser7[index] = otherlist[0][:-2]
        ser8[index] = otherlist[2]
        try:
            ser9[index], ser10[index] = otherlist[-1].split('建')
        except:
            ser10[index] = otherlist[-1]
        ser11[index] = int(houseinfo.find('span', class_='num').string)
        index += 1

frame = DataFrame({ser1.name: ser1, ser2.name: ser2, ser3.name: ser3, \
                   ser4.name: ser4, ser5.name: ser5, ser6.name: ser6, \
                   ser7.name: ser7, ser8.name: ser8, ser9.name: ser9, \
                   ser10.name: ser10, ser11.name: ser11})

path = '链家租房.xlsx'
frame.to_excel(path)