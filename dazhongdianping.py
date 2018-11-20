#- coding:utf-8 -*-
# import selenium
# import requests
# from selenium import webdriver
import pymongo
import requests,codecs
import pymongo,time
from lxml import  html
from multiprocessing import Pool

#自动化模拟
# browser = webdriver.Chrome()
# browser.get('https://www.dianping.com/search/keyword/5/0_南京北京东路57号')

client=pymongo.MongoClient('mongodb://localhost:27017')
db=client['dianping']
myset=db['dianping_zz']
def get_content(j):
    #用于模拟HTTP头的user-agent
    headers = {
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    }

    print('正在爬取第{}页，还剩{}页'.format(j,10000-j))
    url = 'http://www.dianping.com/nanjing/ch0/p{}'.format(j)
    r=requests.get(url)
    r=html.fromstring(r.text)

    lenth=len(r.xpath('//html/body/div[2]/div[3]/div[1]/div[1]'))
    try:
        for i in range(1,lenth+1):
            community=r.xpath('//*[@id="shop-all-list"]/ul/li[3]/div[2]/div[{}]/a[1]/h4/text()'.format(i))[0]
            drr=r.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[{}]/span/text()'.format(i))[0]
            drr2=r.xpath('//*[@id="shop-all-list"]/ul/li[2]/div[2]/div[3]/a[{}]/span/text()'.format(i))[0]
            style=r.xpath('//*[@id="shop-all-list"]/ul/li[7]/div[2]/div[3]/a[{}]/span/text()'.format(i))[0]
            price=r.xpath('//*[@id="shop-all-list"]/ul/li[15]/div[2]/div[2]/a[{}]/b/text()'.format(i))[0]


            info = {'community':community,'drr':drr,'drr2':drr2,'style':style,'price':price}


            try:
                myset.insert(info)
            except:
                print('写入失败')
    except Exception as e :
        print(e)
        print('爬取失败')

    def savetoexcel(output):
        try:
            f = codecs.open('dp_nj.csv', 'a+', 'utf-8')
            f.write(output)
            f.close()
        except Exception as e:
            print('写入失败')

if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.map(get_content, list(range(1, 101)))
    pool.close()
    pool.join()

