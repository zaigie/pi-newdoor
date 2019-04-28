#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in9b
from bs4 import BeautifulSoup   #用来代替正则表达式取源码中相应标签的内容
import random
import requests #用来抓取网页的html源代码
import socket #用做异常处理
import time
import http.client #用做异常处理
import csv
import os
import sys
from PIL import Image,ImageDraw,ImageFont
import traceback
#import re


def get_html(url,data=None):
    """
    模拟浏览器来获取网页的html代码
    """
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    #设定超时时间，取随机数是因为防止被网站认为是爬虫
    timeout=random.choice(range(80,180))
    while True:
        try:
            rep=requests.get(url,headers=header,timeout=timeout)
            rep.encoding="utf-8"
            break
        except socket.timeout as e:
            print("3:",e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print("4:",e)
            time.sleep(random.choice(range(20,60)))
        except http.client.BadStatusLine as e:
            print("5:",e)
            time.sleep(random.choice(range(30,80)))

        except http.client.IncompleteRead as e:
            print("6:",e)
            time.sleep(random.choice(range(5,15)))

    return rep.text

def get_data(html_txt):
    final=[]
    bs=BeautifulSoup(html_txt,"html.parser")   #创建BeautifulSoup对象
    body=bs.body   #获取body部分
    data=body.find("div",{"id":"7d"}) #找到id为7d的div
    ul=data.find("ul")  #获取ul部分
    li=ul.find_all("li")   #获取所有的li

    for day in li:  #对每个标签中的内容进行遍历
        temp=[]
        date=day.find("h1").string   #获取日期
        temp.append(date)   #将日期添加到temp 中
        inf=day.find_all("p")   #找到li中的所有p标签
        temp.append(inf[0].string)   #将第一个p标签中的内容添加到temp列表中红
        if inf[1].find("span") is None:
            temperature_high=None   #傍晚没有最高气温
        else:
            temperature_high=inf[1].find("span").string  #最高气温
            temperature_high=temperature_high.replace("℃","")
        temperature_lower=inf[1].find("i").string   #找到最低温
        temperature_lower=temperature_lower.replace("℃","")
        temp.append(temperature_high)
        temp.append(temperature_lower)
        final.append(temp)   #将temp添加到final中

    return final

def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)

def delete_data(name):
    file_name = name
    if os.path.exists(file_name):
        os.remove(file_name)

if __name__=="__main__":
    url="http://www.weather.com.cn/weather/101271610.shtml"
    html=get_html(url)
    result=get_data(html)
    delete_data("weather.csv")
    write_data(result,"weather.csv")
    day1_weather = result[0][1]
    day1_high = result[0][3]
    day1_low = result[0][2]
    day2_weather = result[1][1]
    day2_high = result[1][3]
    day2_low = result[1][2]
    day1 = '今天:' + '  ' + str(day1_weather)
    day1_temp = str(day1_high) + '~' + str(day1_low) + ' ' + '摄氏度'
    day2 = '明天:' + '  ' + str(day2_weather)
    day2_temp = str(day2_high) + '~' + str(day2_low) + ' ' + '摄氏度'
    f = open('home.txt')
    msg = f.read()
    f.close()
    try:
        epd = epd2in9b.EPD()
        epd.init()
        print("clear")
        epd.Clear(0xFF)
    
        # Drawing on the Horizontal image
        HBlackimage = Image.new('1', (epd2in9b.EPD_HEIGHT, epd2in9b.EPD_WIDTH), 255)  # 298*126
        HRedimage = Image.new('1', (epd2in9b.EPD_HEIGHT, epd2in9b.EPD_WIDTH), 255)  # 298*126
        
        '''#tqicon
        qing = Image.open('/tqicon/qing.bmp')
        duoyun = Image.open('/tqicon/duoyun.bmp')
        yin = Image.open('/tqicon/yin.bmp')
        wu = Image.open('/tqicon/wu.bmp')
        xue = Image.open('/tqicon/xue.bmp')
        xiaoyu = Image.open('/tqicon/xiaoyu.bmp')
        zhongyu = Image.open('/tqicon/zhongyu.bmp')
        dayu = Image.open('/tqicon/dayu.bmp')
        leizhenyu = Image.open('/tqicon/leizhenyu.bmp')
        
        icon = re.findall(,str(day1_weather))'''
        
    
        # Horizontal
        print("Drawing")
        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRedimage)
        font16 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 16)
        font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 18)
        font14 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 14)
        drawblack.line((0,100,298,100), fill = 0)
        drawblack.line((266,0,266,198), fill = 0)
        drawblack.text((105, 5),day1, font = font18, fill = 0)
        drawred.text((105, 25), day1_temp, font = font18, fill = 0)
        drawblack.text((105, 55),day2, font = font18, fill = 0)
        drawred.text((105, 75), day2_temp, font = font18, fill = 0)
        drawblack.text((5,105),msg,font = font16, fill = 0)
        drawblack.text((12,75),u'天气预报',font = font16, fill = 0)
        drawred.chord((275,110,285,120),0,360,fill = 0)
        drawblack.text((275,5),u'4',font = font14, fill = 0)
        drawblack.text((275,20),u'0',font = font14, fill = 0)
        drawblack.text((275,35),u'5',font = font14, fill = 0)
        drawblack.text((275,50),u'R',font = font14, fill = 0)
        drawblack.text((275,65),u'U',font = font14, fill = 0)
        drawblack.text((275,80),u'N',font = font14, fill = 0)
        qing = Image.open('weather.bmp')
        HRedimage.paste(qing,(10,5))
        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
        time.sleep(2)
    
        epd.sleep()
        
    except:
        print('traceback.format_exc():\n%s',traceback.format_exc())
        exit()
