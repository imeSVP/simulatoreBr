#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# globals_and_constants.py

from pathlib import Path


csvFolderPath = 'csvdata' 
testValue = 100

WEBDRIVER_LOC = str(Path(__file__).parent.resolve()/'chromedriver')
# WEBDRIVER_LOC = 'chromedriver.exe'

MYSQL = {'host': '146.59.233.56', 'user': 'finser', 'passwd': 'finser0914?',
         'db': 'finser_banks_db', 'use_unicode': True,
         'charset': 'utf8mb4','local_infile':1}



dbTable = {'inputCompass':"input_simulatori_compass",
           'inputAgos':"input_simulatori_agos",
           'inputUnicredit':"input_simulatori_unicredit",
           'inputTbGeneralita':"finser_banks_db.generalita",
           'outputTb':'output_simulatori',
           'outputTbRam':'output_simulatori_ram'
           }
DEBIAN = {'hostname': '146.59.233.56', 'username': 'servern',
          'password': 'Chi1456?'}

countries = [
    #"CH",
    "IT",
    #"DE",
    #"FR",
    #"UK",
    #"AT",
    #"NL",
    #"ES",
    #"PL",
    #"KR",
    #"BG",
    #"FI",
    #"HR"
  ];
INIT_PORTS = [1080]
ENDPOINT = "proxy.goproxies.com"
COUNTRY = "IT"
USERNAME = "customer-imetrics-country-it"
PASSWORD = "eddd26be6a43b9d6470b466ab19ef325"

TWOCAPTCHA_KEY = '3da74b773dc0832937e86caa8e85cfff'

plugin_file = 'proxy_auth_plugin.zip'

homePageUrl = "https://www.mutuionline.it"
__USER_DATE_DIR_PATH__ = str(Path(__file__))
browser_Path = '/usr/bin/brave-browser'
browser_args = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-infobars',
    '--disable-dev-shm-usage',
    '--disable-brave-shields-up'
    '--disable-blink-features=AutomationControlled',
    '--window-size=1280,800',  # 动态设置窗口大小
]

defValue = None
headersz = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-encoding': 'gzip, deflate, br, zstd',
  'accept-language': 'it-IT,it;q=0.9',
  'cache-control': 'no-cache',
  'content-type': 'application/x-www-form-urlencoded',
  'origin': 'https://tariffe.segugio.it',
  'pragma': 'no-cache',
  'referer': 'https://tariffe.segugio.it/luce-gas/?',
  'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}





def _init():#初始化
    global _global_dict
    _global_dict = {
        "global_log":"",
        "cookie_value":"",
        "PORTS": INIT_PORTS,
        "headerDic": headersz
    }


def set_value(key,value):
    """ 定义一个全局变量 """
    global _global_dict
    _global_dict[key] = value


def get_value(key,defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """

    global _global_dict
    try:
        return _global_dict[key]
    except KeyError:
        return defValue

