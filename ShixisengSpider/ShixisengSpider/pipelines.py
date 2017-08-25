# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ShixisengspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            db=settings['MYSQL_DBNAME'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        #返回实例化的cls对象
        return cls(dbpool)

    def do_insert(self, cursor, item):
        if 'is_expired' in item:
            print('xxxx')
            return

        insert_sql = """
                    insert into ciweishixi_article(title, job_type, pub_time, stop_time,
                                                    job_city, degree, salary_min, salary_max,
                                                    job_info, job_advantage, job_duty, job_required,
                                                    url_object_id, url, company_position, crawl_time,
                                                    company_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item['title'], item['job_type'], item['pub_time'], item['stop_time'],
                                    item['job_city'], item['degree'], item['salary'][0], item['salary'][1],
                                    item['job_info'], item['job_advantage'], item['job_duty'], item['job_required'],
                                    item['url_object_id'], item['url'], item['company_position'], item['crawl_time'],
                                    item['company_url']))

    def handle_error(self, failure):
        #处理异步操作的异常
        pass

    def process_item(self, item, spider):
        #使用异步操作执行数据库操作
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
