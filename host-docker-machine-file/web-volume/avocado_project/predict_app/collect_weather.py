# coding=utf-8

import requests
from bs4 import BeautifulSoup
import json
import os





#python파일의 위치
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('http://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09620101')
html = req.text
soup = BeautifulSoup(html, 'html.parser')
wea = soup.find_all("li", {"class":"info"})

w = list(wea)

print(u"{}".format(str(w[0])))

ws = list(str(i).encode("utf-8") for i in w)

print(ws)

today_am = (wea[0].text).split("강수확률 ")
today_pm = (wea[1].text).split("강수확률 ")
tomor_am = (wea[2].text).split("강수확률 ")
tomor_pm = (wea[3].text).split("강수확률 ")

weather = [today_am, today_pm, tomor_am, tomor_pm]

for i in weather:
    print(i)