# -*- coding: utf-8 -*-
# /usr/bin/env python
# coding=utf8

# c后面是车型论坛编号从45开始！！
# http://club.autohome.com.cn/bbs/forum-c-45-1.html

import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
# @Author: levenls
# @Date:   2016-09-29 17:27:41
# @Last Modified by:   leven-ls
# @Last Modified time: 2016-10-07 17:07:15
import re
import pickle
import os.path
import datetime
import time
import random
import requests
from datetime import datetime,date,timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import pprint
import pyodbc
# cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=LianJia')
# cursor = cnxn.cursor()
batchLoadTime = datetime.now()
today = date.today()
print 'Load Time',batchLoadTime

#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

def start():
    # print grabedPool["data"]
    for i in xrange(1, 101):
        page = "http://www.xcar.com.cn/bbs/viewthread.php?tid=".format(str(i))
        # grab(page)
#http://www.xcar.com.cn/bbs/viewthread.php?tid=29564777

startPage = 29554740
endPage = startPage+100


for i in xrange(startPage, endPage):
    page = "http://www.xcar.com.cn/bbs/viewthread.php?tid=".format(str(i))
    print '[Page] / [PageURL] / [Start Page]',page,'/', i
    response = requests.get(page, headers=hds[random.randint(0, len(hds) - 1)])
    html = requests.get(page)
    soup = BeautifulSoup(html.text.encode(html.encoding), 'lxml', from_encoding='utf-8')
    tradedHoustList = soup.find("h1", class_="title")
    print tradedHoustList