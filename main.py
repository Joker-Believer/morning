from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id_susu = os.environ["USER_ID_SUSU"]
user_id_ya = os.environ["USER_ID_YA"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  url = "https://v0.yiketianqi.com/api?unescape=1&version=v62&appid=65516522&appsecret=Q93NXjBS&city=" + city 
  res = requests.get(url).json()
  return res

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_words2():
  url = "http://open.iciba.com/dsapi/"
  r = requests.get(url)
  content = r.json()['content']
  note = r.json()['note']
  return note


def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather = get_weather()
data = {
        "weather":{"value":weather['wea_day']}
        ,"low":{"value":str(math.floor(weather['tem2'])) + "℃", "color": "#1E90FF"}
        ,"high":{"value":str(math.floor(weather['tem1'])) + "℃", "color": "#FF0000"}
        ,"love_days":{"value":get_count(), "color": "#FFB6C1"}
        ,"birthday_left":{"value":get_birthday()}
        ,"words":{"value":get_words(), "color":get_random_color()}
        ,"words2":{"value":get_words2(), "color":get_random_color()}
        ,"date":{"value":weather['date']}
        ,"week":{"value":weather['week']}
        ,"weather_words":{"value":weather['air_tips'], "color":get_random_color()}
       }

res = wm.send_template(user_id_susu, template_id, data)
res = wm.send_template(user_id_ya, template_id, data)

print(res)
