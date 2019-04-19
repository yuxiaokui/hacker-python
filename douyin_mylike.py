# -*- coding: cp936 -*-
import pychrome
import random
import requests
import time
import json
import re

headlessServers = ["http://localhost:9222"]

home_url = 'https://www.iesdouyin.com/share/user/71148817607'

headlessServer = random.choice(headlessServers)

browser = pychrome.Browser(url=headlessServer)

tabs = browser.list_tab()

if not tabs:
    tab = browser.new_tab()
else:
    tab = tabs[0]


fav_url = ''

def request_will_be_sent(**kwargs):
    global fav_url
    url = kwargs.get('request').get('url')
    if 'dytk' in url:
        fav_url = url.replace('post','favorite')
        
tab.set_listener("Network.requestWillBeSent", request_will_be_sent)

tab.start()
tab.Network.enable()
tab.Page.navigate(url=home_url, _timeout=5)
tab.wait(timeout=1)
time.sleep(2)

tab.Page.navigate(url=fav_url, _timeout=5)
tab.wait(timeout=1)
res = tab.Runtime.evaluate(expression='document.documentElement.outerHTML')
result = res["result"]["value"]

regex = re.compile(r"video_id=(.*?)&")

r = regex.findall(result)

r =  list(set(r))

for i in r :
    headers = {'User-Agent':'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;AvantBrowser)'}
    mp4_url = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" +i+ "&app_name=&device_id=1&channel=&aid=&os_version=&device_platform=&build_number=&device_type="
    print mp4_url
