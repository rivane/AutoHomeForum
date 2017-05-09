# -*- coding: utf-8 -*-
# /usr/bin/env python
# coding=utf8
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
import re
import pickle
import os.path
import datetime
import time
import random
import requests
from datetime import datetime,date,timedelta
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
opts = Options()
prefs = {"profile.managed_default_content_settings.images":2} # this will disable image loading in the browser
opts.add_experimental_option("prefs",prefs)  # Added preference into chrome options
opts.add_argument("user-agent="'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
#added chrome option user-agent
# driver = webdriver.Chrome('chromedriver.exe', chrome_options=opts)  # finally add these option
from bs4 import BeautifulSoup
import pprint
import pyodbc
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=AutoHomeForum')
cursor = cnxn.cursor()
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

pgHead = "http://club.autohome.com.cn/bbs/forum-c-65-"
pgTail = ".html?orderby=dateline&qaType=0"
# c后面是车型论坛编号从45开始！！
# http://club.autohome.com.cn/bbs/forum-c-45-1.html

maxPage = 681 #每个论坛只保存1000页最多，每次从最后一页开始遍历
driver = webdriver.Chrome(chrome_options=opts)
# driver.set_window_size('200','100') #设置浏览器宽480，高800
driver.set_window_size('800','300') #设置浏览器宽480，高800
for i in range(maxPage,0,-1):
    print i
    page = pgHead+str(i)+pgTail
    print 'PageID: ',i,'URL',page,'\n'
    driver.get(page);
    onePageList = driver.find_elements_by_class_name('list_dl')
    for topic in onePageList:
        topicItems = topic.get_attribute('lang').split("|")
        if len(topicItems) <> 1:
            print 'PageID: ',i,'PageURL',page,'Topic ID',onePageList.index(topic)
            postURL = topic.find_element_by_class_name('a_topic').get_attribute('href')
            cursor.execute("select distinct PostURL from [AutoHomeForum].[dbo].FactTopic where PostURL=?",
                           str(postURL))
            sumCheck = cursor.fetchall()
            print sumCheck[0]
            if len(sumCheck) < 1:
                submitTime = datetime.now()
                try:
                    print topicItems[0],topicItems[1],topicItems[2]
                    print 'URL: ',postURL
                    postTitle = topic.find_element_by_class_name('a_topic').text
                    print 'Title: ',postTitle
                    lastReplyTime = topic.find_element_by_class_name('ttime').text
                    print 'Last Reply Date Time: ',lastReplyTime
                    lastReplyNickName = topic.find_element_by_class_name('linkblack').text
                    print 'Last Reply Nick Name: ', lastReplyNickName
                    clickCount = topic.find_element_by_class_name('tcount').text
                    print 'Click Count: ',clickCount
                    if len(clickCount.strip().replace(' ',''))==0:
                        clickCount=0
                    print '\n'
                    cursor.execute(
                        "insert into [FactTopic]([Class],[ForumID],[PostID],[ReplyCount],[PublishDateTime],[PostOwnerID],[LastReplyerID],[unknow01],[unknow02],[unknow03],[PostOwnerNickName],[unknow04],[PublishDateTime2],[unknow05],[PicPreview],[PostURL],[PostTitle],[LastReplyDateTime],[LastReplyNickName],[ClickCount],[BatchDateTime],[SubmitDateTime]) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        str(topicItems[0]),topicItems[1],topicItems[2],topicItems[3],topicItems[4],topicItems[5],topicItems[6],topicItems[7],topicItems[8],topicItems[9],topicItems[10],topicItems[11],topicItems[12],topicItems[13],topicItems[14],str(postURL), str(postTitle).decode('utf-8'), str(lastReplyTime), str(lastReplyNickName).decode('utf-8'),int(clickCount), batchLoadTime,submitTime)
                    cnxn.commit()
                except Exception as e:
                    print e
    time.sleep(2)