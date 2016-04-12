# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
import urllib2
from scrapy.exceptions import DropItem

class PostgresPipeline(object):

    def __init__(self):
        import psycopg2
        self.conn = psycopg2.connect(user="postgres",
                                     password="postgres",
                                     dbname="CMS",
                                     host='localhost')

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        cursor.execute("insert into first_cms ( url, title, cms, title_without_url ) values (%s, %s, %s, %s)",
                       [
                           item['url'][0],
                           item["title"][0],
                           item["cms"],
                           item["title_without_url"][0]
                       ])
        self.conn.commit()
        return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.url_seen = []

    def process_item(self, item, spider):
        if item['url'] in self.url_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.url_seen.append(item['url'])
            return item

