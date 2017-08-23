# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from urllib import parse
from NbaSpider.items import NbaArticleItem
import datetime
import time

from NbaSpider.utils.common import get_md5


class NbaSpider(scrapy.Spider):
    name = 'nba'

    #allowed_domains = ['https://voice.hupu.com/nba']
    start_urls = ['https://voice.hupu.com/nba/']

    def parse(self, response):
        #程序启动时候 先爬取hoop的Nba体育页表页
        #假设这里有60个页面
        post_page = response.css('div.list-hd h4 a::attr(href)').extract()

        #遍历处理这60个页面
        for post_url in post_page:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        #经过遍历完60个页面之后 返回parse继续爬取一个列表页
        next_page = response.css('.page-btn-prev ::attr(href)').extract_first('')
        if next_page:
            yield Request(url=parse.urljoin(response.url, next_page), callback=self.parse)

    def parse_detail(self, response):
        title = response.css('div.artical-title h1::text').extract_first('').strip()
        source = response.css('#source_baidu a::text').extract_first('')

        str_time = response.css('#pubtime_baidu::text').extract_first('').strip()
        create_time = ''
        try:
            tmp = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            y, m, d, a, b, c = tmp[0:6]
            create_time = datetime.datetime(y, m, d, a, b, c)
        except Exception as e:
            create_time = datetime.datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

        editor = response.css('#editor_baidu::text').extract_first('')
        match_object = re.match(r".*编辑：(.*)\)", editor)
        if match_object:
            editor = match_object.group(1)
        else:
            editor = ''
        content_list = response.css('.artical-main-content p::text').extract()
        content = ".".join(content_list)
        image_url = response.css('.artical-importantPic img::attr(src)').extract_first('')

        article_item = NbaArticleItem()
        article_item['title'] = title
        article_item['source'] = source
        article_item['create_time'] = create_time
        article_item['editor'] = editor
        article_item['content'] = content
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)
        article_item['image_url'] = [image_url]

        #将其传递pipe， 用于保存数据
        yield article_item
