# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NbaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NbaArticleItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    create_time = scrapy.Field()
    editor = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field() #图片在本地的存放路径

