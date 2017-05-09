# -*- coding: utf-8 -*-
# /usr/bin/env python
# coding=utf8
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
import socket
import errno
import re
import pickle
import os.path
import datetime
import time
import random
import requests
from datetime import datetime,date,timedelta

# from nltk import sent_tokenize, word_tokenize, pos_tag
# from nltk.corpus import sinica_treebank
# from sklearn.feature_extraction import DictVectorizer
# from nltk.corpus import treebank
# import nltk
# from nltk.stem import WordNetLemmatizer
# wordnet_lemmatizer = WordNetLemmatizer()
# import jieba
# # 感觉是load是加载上用户自定义词典，但是还是优先用默认词典，而set是把自定义词典优先考虑，所以设置了set应该就不用再load，而load之后还是需要set才能保证优先级。
# mydcv = 'c://python27/Lib/site-packages/jieba/dict_Original_Car.txt'
# jieba.load_userdict(mydcv)
# jieba.set_dictionary(mydcv)
# import jieba.analyse
# # 只针对analysis部分好用，不涉及cut部分，所以cut完还在，但是idf评分那块就没有它了
# # sw = 'c://python27/Lib/site-packages/jieba/stop_words.txt'
# # jieba.analyse.set_stop_words(sw)
# import jieba.posseg as pseg
# # jieba.add_word("韩笑", freq=1, tag=None)
# # 更改切词的分隔符，比如正常是句号，可以改成空格或者逗号等等，好使
# myToken = 'c://python27/Lib/site-packages/jieba/dictToken.txt'
# jieba.Tokenizer(dictionary=myToken)
# # 更改语料库IDF好使，需要仔细观察weight权重评分会发生变化
# jieba.analyse.set_idf_path("c://python27/Lib/site-packages/jieba/myIDF.txt")
# # allowPOS = ("nn", "n", "nr", "pn", "cd", "j", "ns", "ni", "r", "nd")

#test row for github
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
opts = Options()
prefs = {"profile.managed_default_content_settings.images":2} # this will disable image loading in the browser
opts.add_experimental_option("prefs",prefs)  # Added preference into chrome options
opts.add_argument("user-agent="'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
#added chrome option user-agent
# driver = webdriver.Chrome('chromedriver.exe', chrome_options=opts)  # finally add these option
from bs4 import BeautifulSoup
import pyodbc
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=autohomeforum')
cursor = cnxn.cursor()
batchLoadTime = datetime.now()
today = date.today()
print 'Load Time',batchLoadTime

filePath = 'C:/webPic/'
fileType = '.txt'
bmw5Txt = filePath + 'bmw5corpus' + fileType

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



# singlePage = "http://club.autohome.com.cn/bbs/thread-c-65-61952148-1.html#pvareaid=2199101"

cursor.execute("select max(PostID) from [AutoHomeForum].[dbo].[FactAllPosts]")
lastPostID = cursor.fetchall()[0]
print 'Last Porcessed POST ID: ', lastPostID

######从第n次开始
cursor.execute("select id,posturl from [FactTopic] where id > ? order by id", lastPostID)

#####第一次从零开始
# cursor.execute("truncate table [FactAllPosts]")
# cursor.execute("select id,posturl from [FactTopic] order by id")

urls = cursor.fetchall()
print  len(urls),' posts to be processed...'
# for i in range(len(urls)):
#     print urls[i][0]
#     print urls[i][1]

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

driver = webdriver.Chrome(chrome_options=opts)
driver.set_window_size('800', '300')  # 设置浏览器宽480，高800
for i in range(len(urls)):
    print 'URL======================',urls[i][1]
    cursor.execute("select distinct postid from [AutoHomeForum].[dbo].FactAllposts where postid=?",
                   str(urls[i][0]))
    sumCheck = cursor.fetchall()
    print sumCheck
    # sumCheck = []

    if len(sumCheck) < 1:
        driver.get(urls[i][1])
        allUserInfo = driver.find_elements_by_css_selector(".conleft.fl")
        allPosts = driver.find_elements_by_css_selector(".clearfix.contstxt.outer-section")
        # allUsers = driver.find_element_by_css_selector(".txtcenter.fw")
        # F1 > div.conleft.fl > ul.maxw > li.txtcenter.fw
        for post in allPosts:
            uid = post.get_attribute("uid")
            print 'User ID: ', uid
            allUserInfo = post.find_elements_by_class_name("leftlist")
            for userInfo in allUserInfo:
                print 'URL ID: ',i
                print 'full user info: ', userInfo.text
                rows = userInfo.text.split("\n")
                regDate = ''
                userResi =''
                ownedBrand = ''
                watchingBrand = ''
                for rowTxt in rows:
                    if rowTxt.find(u"注册")!=-1:
                        regDate = rowTxt.replace(u"注册：","").replace(u"年",'-').replace(u'月','-').replace(u'日','')
                        print '注册时间： ', regDate
                    if rowTxt.find(u"来自")!=-1:
                        print '用户地区： ',rowTxt.replace(u"来自：","")
                        userResi = rowTxt.replace(u"来自：","").decode('utf-8')
                    if rowTxt.find(u"爱车") != -1:
                        print '爱车品牌： ', rowTxt.replace(u"爱车：","")
                        ownedBrand = rowTxt.replace(u"爱车：","")
                    if rowTxt.find(u"关注") != -1 and rowTxt.find(u"加关注") == -1:
                        print '关注品牌： ', rowTxt.replace(u"关注：","")
                        watchingBrand = rowTxt.replace(u"关注：", "")

            cursor.execute(
                "insert into [FactAllPosts]([PostID],[PostOwnerID],[RegDate],[UserLocation],[PossessCarBrand],[WatchingCarBrand]) values (?,?,?,?,?,?)",
                urls[i][0], uid, regDate, str(userResi).decode('utf-8'), str(ownedBrand).decode('utf-8'),str(watchingBrand).decode('utf-8')
            )
            cnxn.commit()
            print 'rows saved...and date is: ', regDate

        allText = driver.find_elements_by_class_name("w740")
        postText = ''
        for text in allText:
            try:
                if text.find_element_by_class_name("yy_reply_cont"):
                    replyText = text.find_element_by_class_name("yy_reply_cont").text
                    match = zhPattern.search(replyText)
                    if match:
                        # originText = text.find_element_by_class_name("rrlycontxt").text
                        # qANDa = originText + '\n' + replyText
                        # print 'reply with original comment: ','\n',qANDa
                        postText = postText + '\n'+ replyText
                        # postText = replyText + '\n'
            except NoSuchElementException as noE:
                match = zhPattern.search(text.text)
                if match:
                    # print 'No Reply Text: ',text.text
                    postText = postText + '\n' + text.text
                    # postText = text.text + '\n'
            except Exception as e:
                print e

        print urls[i][0]
        print postText.replace('\n\n','\n'),'\n\n\n\n'
        cursor.execute("update FactTopic set PostText=? where id=?", str(postText).decode('utf-8'), urls[i][0])
        cnxn.commit()
        print 'Post Text Saved to Database...'

        # f = open(bmw5Txt, 'a+')
        # f.write(postText)
        # f.close()
        # print 'post text saved!'

    else:
        print 'Something is wrong'

    time.sleep(2)

