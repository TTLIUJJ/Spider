# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ShixisengSpider.items import ShixisengItemLoader, ShixisengItem
from ShixisengSpider.utils.common import get_md5
from datetime import datetime


class ShixisengSpider(CrawlSpider):
    name = 'shixiseng'
    allowed_domains = ['www.ciweishixi.com']
    start_urls = ['http://www.ciweishixi.com']

    rules = (
        Rule(LinkExtractor(allow=r'job/.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item_loader = ShixisengItemLoader(item=ShixisengItem(), response=response)

        item_loader.add_xpath('title', '//div[@class="widget-job-base"]/h2/text()')
        item_loader.add_xpath('job_type', '//div[@class="widget-job-base"]/h2/i/@title')
        item_loader.add_xpath('pub_time', '//div[@class="widget-job-base"]/time[1]/text()')
        item_loader.add_xpath('salary', '//span[@class="wage"]/b/text()')
        item_loader.add_xpath('job_city', '//div[@class="widget-job-base"]/div[@class="info"]/span[2]/text()')
        item_loader.add_xpath('degree', '//div[@class="widget-job-base"]/div[@class="info"]/span[3]/text()')
        item_loader.add_xpath('stop_time', '//div[@class="widget-job-base"]/time[2]/text()')
        item_loader.add_xpath('job_info', '//div[@class="subinfo"]/span[not(@class)]/text()')
        item_loader.add_xpath('job_advantage', '//div[@class="widget-job-tags"]/div/span/text()')
        item_loader.add_xpath('job_duty', '//div[@class="widget-job-desc"]/div[1]/p/text()')
        item_loader.add_xpath('job_required', '//div[@class="widget-job-desc"]/div[2]/p/text()')
        item_loader.add_xpath('company_position', '//span[@class="block"]/text()')
        item_loader.add_xpath('is_expired', '//div[@class="widget-job-base"]/span/@class')
        item_loader.add_xpath('company_url', '//div[@class="widget-jobinfo"]/dl[2]/dd/a/@href')

        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_value('crawl_time', datetime.now())

        job_item = item_loader.load_item()

        return job_item

