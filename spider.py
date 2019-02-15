# -*- coding: utf-8 -*-
"""
Created on Thur Feb  14 11:49:02 2019

@author: songdongdong
"""

'''
数据的获取
影评数据来源于豆瓣。
但是豆瓣的反爬机制实在精致，大量爬取数据还会有法律风险，所以就小规模获取了600条数据。
高分评价、中等评价和低分评价，各自占了200条，对各个分数段的评价做到平等对待。
https://mbd.baidu.com/newspage/data/landingshare?pageType=1&isBdboxFrom=1&context=%7B"nid"%3A"news_9960210956876342565"%2C"sourceFrom"%3A"bjh"%7D
'''

import requests
import re
import time
import pandas as pd

class Spider:
    """
    模拟登录，爬取豆瓣影评数据
    """
    def __init__(self, username, password):
        """
        构造器，并模拟登录
        :param username: 豆瓣账号
        :param password: 豆瓣密码
        """
        self.__username = username #登录名
        self.__password = password #登录密码
        self.loginURL = 'https://www.douban.com/' #post地址
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36','Referer': 'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001'}
        self.data = {'source': 'index_nav', 'form_email': self.__username, 'form_password': self.__password, 'Connection': 'keep-alive'} #post数据
        self.session = requests.Session() #session对象
        self.session.headers.update(self.headers)
        self.resp = self.session.post(self.loginURL, data = self.data, headers = self.headers) #模拟登录
    
    def __getContent(self, url):
        """
        私有属性，获取url的html
        :param url: 需要获取的网页url地址
        :return html: 返回网页html字符串
        """
        html = self.session.get(url, headers = self.headers).content.decode('utf-8')
        return html
    
    def getComments(self, url):
        """
        获取影评数据
        :param url: 网页的url
        :return comments: 影评列表
        """
        html = self.__getContent(url)
        pattern = '<span class="short">(.*?)</span>'
        comments = re.findall(pattern, html)
        return comments

if __name__ == '__main__':
    # url模式的定义
    typePattern1 = 'https://movie.douban.com/subject/26266893/comments?start='
    typePattern2 = '&limit=20&sort=new_score&status=P&percent_type='

    hNum = 200  # 好评数量
    mNum = 200  # 中评数量
    lNum = 200  # 差评数量

    spd = Spider('695492835@qq.com', 'sjyttkl1015@')  # 定义对象

    hComments = []
    mComments = []
    lComments = []

    # 生成URL列表
    urlList1 = [typePattern1+str(i)+typePattern2+'h' for i in range(0, hNum, 20)]
    urlList2 = [typePattern1+str(i)+typePattern2+'m' for i in range(0, mNum, 20)]
    urlList3 = [typePattern1+str(i)+typePattern2+'l' for i in range(0, lNum, 20)]
    
    for url in urlList1:
        hComments = hComments + spd.getComments(url)
        print('正在爬取好评第',len(hComments), '条')
        time.sleep(1)
    
    for url in urlList2:
        mComments = mComments + spd.getComments(url)
        print('正在爬取中评第', len(mComments), '条')
        time.sleep(1)
        
    for url in urlList3:
        lComments = lComments + spd.getComments(url)
        print('正在爬取差评第', len(lComments), '条')
        time.sleep(1)

    # 存入txt文件
    df1 = pd.DataFrame(hComments)
    df1.to_csv('hComments.txt', index=None, header=None)
    
    df2 = pd.DataFrame(mComments)
    df2.to_csv('mComments.txt', index=None, header=None)
    
    df3 = pd.DataFrame(lComments)
    df3.to_csv('lComments.txt', index=None, header=None)

        
        
    
        
        
    
    
        
        
    
    
        
        
        