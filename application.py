# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import json
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

ifttt_key = 'cgcFQMktW46bFG9exR5nta'
event = 'get_weather'
url_ifttt = 'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(event,ifttt_key)

sched = BlockingScheduler(timezone="Asia/Taipei")

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=2, minute=25, misfire_grace_time=3600)
# @sched.scheduled_job('interval', seconds = 5, misfire_grace_time=3600)
def scheduled_job(city='新竹市'):
    self.cst = datetime.timezone(datetime.timedelta(hours=+8))
    # ------ get weather ------
    token = 'CWB-034ACAFB-7E97-43C6-8611-E5B6DF04A68D' 
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(city)
    Data = requests.get(url)
    weather   = (json.loads(Data.text,encoding='utf-8'))['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
    rain_rate = (json.loads(Data.text,encoding='utf-8'))['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName']
    min_temp  = (json.loads(Data.text,encoding='utf-8'))['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName']
    max_temp  = (json.loads(Data.text,encoding='utf-8'))['records']['location'][0]['weatherElement'][4]['time'][0]['parameter']['parameterName']
    now_time = datetime.datetime.now(self.cst).strftime("%Y-%m-%d %H:%M:%S")
    message = f'{now_time}<br>--12小時內天氣預報--<br><br>{weather}<br>氣溫{min_temp}~{max_temp}°C<br>降雨機率{rain_rate}%<br><br>'
    url_ifttt_to_send = f'{url_ifttt}?value1={message}'
    print(url_ifttt_to_send)
    res = requests.get(url_ifttt_to_send)
    print(res)

    # print(weather)
    # print(rain_rate)
    # print(min_temp)
    # print(max_temp)
    # return (Data.text)


     # ------ one sentence ------
    # get target day (2021/02/07 ~ 2021/5/17)
    today = datetime.date.today()
    delta_day = datetime.timedelta(days=263)
    target_day = (today - delta_day).strftime('%Y%m%d')

    # get sentence and author
    url = f"https://tw.feature.appledaily.com/collection/dailyquote/{target_day}"
    print(url)

    html = requests.get(url)
    html.encoding="utf-8"
    sp = BeautifulSoup(html.text,"html.parser")
    sentence = str(sp.find("p"))
    author = str(sp.find("h1"))

    remove_list = ["<p>", "</p>", "<br/>", "<h1>", "</h1>", "\n", "  "]
    for remove in remove_list:
        if remove in sentence:
            sentence = sentence.replace(remove,"")
        if remove in author:
            author = author.replace(remove,"")
    print(sentence)
    print(author)

    message = f"--Today's sentence--<br><br>{sentence}<br><br>{author}<br><br>"
    url_ifttt_to_send = f'{url_ifttt}?value1={message}'
    print(url_ifttt_to_send)
    res = requests.get(url_ifttt_to_send)
    print(res)


sched.start() 

# get_city_weather('新竹市')

# with open('weather.json', 'w', encoding='utf-8-sig') as file:
#     file.write(get_city_weather('新竹市'))