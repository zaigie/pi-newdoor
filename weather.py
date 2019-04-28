from bs4 import BeautifulSoup   #用来代替正则表达式取源码中相应标签的内容
import random
import requests #用来抓取网页的html源代码
import socket #用做异常处理
import time
import http.client #用做异常处理
import csv

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

def get_url():
    city={
    "xc":"101271610",
    "三亚":"101310201",
    "苏州":"101190401",
    "郑州":"101180101"
    }
    for k in city:
        print(k)
    city_name=input("请输入你要查询的城市名字：")
    city_num=city[city_name]
    weather_url="http://www.weather.com.cn/weather/%s.shtml"%city_num
    return weather_url

if __name__=="__main__":
    # url="http://www.weather.com.cn/weather/101190401.shtml"
    url=get_url()
    html=get_html(url)
    result=get_data(html)
    write_data(result,"weather.csv")
    for i in result:
        print(i)        #打印天气情况