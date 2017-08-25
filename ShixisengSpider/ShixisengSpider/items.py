# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from datetime import datetime


class ShixisengspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ShixisengItemLoader(ItemLoader):
    default_output_processor = TakeFirst()



def process_time(value):
    match_object = re.match(r'.*?(\d.*)', value)
    time = ''
    if match_object:
        match_re = match_object.group(1)
        time = datetime.strptime(match_re, "%Y-%m-%d").date()
    else:
        time = datetime.now()

    return time


def process_salary(value):
    salary = []
    try:
        match_min = re.match(r'.*?(\d+).*', value)
        match_max = re.match(r'.*-(\d+).*', value)
        if match_min and match_max:
            salary.append(int(match_min.group(1)))
            salary.append(int(match_max.group(1)))
    except Exception as e:
        salary = [0, 0]

    return salary


def process_whitespace(value):
    value = value.strip()
    return value


def process_position(value):
    try:
        value = value[5:]
    except Exception as e:
        pass

    return value

def do_nothing(value):
    return value



class ShixisengItem(scrapy.Item):
    title = scrapy.Field()
    job_type = scrapy.Field()
    pub_time = scrapy.Field(
        input_processor=MapCompose(process_time)
    )
    salary = scrapy.Field(
        output_processor=MapCompose(process_salary)
    )
    job_city = scrapy.Field()
    degree = scrapy.Field()
    stop_time = scrapy.Field(
        input_processor=MapCompose(process_time)
    )
    job_info = scrapy.Field(
        input_processor=MapCompose(process_whitespace),
        output_processor=Join('')
    )
    job_advantage = scrapy.Field(
        input_processor=MapCompose(process_whitespace),
        output_processor=Join('')
    )
    job_duty = scrapy.Field(
        input_processor=MapCompose(process_whitespace),
        output_processor=Join('')
    )
    job_required = scrapy.Field(
        input_processor=MapCompose(process_whitespace),
        output_processor=Join('')
    )
    company_position = scrapy.Field(
        input_processor=MapCompose(process_position)
    )
    is_expired = scrapy.Field()
    company_url = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    crawl_time = scrapy.Field()

