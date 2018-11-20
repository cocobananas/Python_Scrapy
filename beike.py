import pymongo
import requests,codecs
import pymongo,time
from lxml import html
from multiprocessing import pool

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['testdb']
myset = db ['beike']
def get_content(j):
    print('正在爬取第{}页，还剩{}页'.format(j,100-j))
    url = 'https://nj.zu.ke.com/zufang/pg{}/#contentList'.format(j)
    r = requests.get(url)
    #r = html.fromstring(r.text)
    print(r)
    #lenth = len(r.xpath(''))