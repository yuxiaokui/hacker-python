# -*- coding: utf-8 -*-
import pymongo
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client['AI']
posts = db['tongji']

datas = posts.find().sort("count",pymongo.DESCENDING).limit(100)
tag = ""

for data in datas:
    tag = tag + data['hanzi'] + u"字" + " "



from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

def finance_cloud(tag):
      tags = make_tags(get_tag_counts(tag),maxsize=100)
      create_tag_image(tags,"cloud.png", size=(1280,800),background=(0, 0, 0, 255), fontname="SimHei")


print tag
finance_cloud(tag)
