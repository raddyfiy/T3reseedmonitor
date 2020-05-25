#!python3
# -*- coding: UTF-8 -*-
#T3续种监测V1.0
#T3nnis reseed monitor V1.0

import requests
import json
import re
from bs4 import BeautifulSoup

username='XXXXXXXXXXX'     #用户名,不要去掉引号
password='XXXXXXXXXXXXX'     #密码,不要去掉引号

checklist=[
'https://t3nnis.tv/details.php?id=13280', #添加链接
'https://t3nnis.tv/details.php?id=17263',
'https://t3nnis.tv/details.php?id=35943',
'https://t3nnis.tv/details.php?id=12221',
]
#暂时手动添加，下一版考虑支持在线同步

def login(session):
    loginurl=('https://t3nnis.tv/takelogin.php')
    headers = {
    'Host': 't3nnis.tv',
    'Connection': 'keep-alive',
    'Content-Length': '35',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://t3nnis.tv',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://t3nnis.tv/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,ru;q=0.2',
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    }
    data={
    'username':username,
    'password':password
    }
    response = session.post(loginurl,data=data,headers=headers)
    if username in response.text:
        print('登录成功,返回url:')
        print(response.url)
    else:
        print('登录失败')
        sys.exit()
    return 0

def check(session):
    headers = {
    'Host': 't3nnis.tv',
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    }
    for checkurl in checklist:
        response=session.get(checkurl,headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        filelistmark=soup.find_all('div',id= "filelist")[0]
        torrentname=filelistmark.find_all('tr')[1].find_all('td')[1].get_text()
        #size=filelistmark.find_all('tr')[1].find_all('td')[2].get_text()
        info=re.findall(r">(.*\(s\) total)",response.text)[0]
        print(checkurl+":   "+str(torrentname)+"    "+info)

session = requests.Session()
login(session)
check(session)
input()     #防止误关