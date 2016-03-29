# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
import urllib2


class PostgresPipeline(object):

    def __init__(self):
        import psycopg2
        self.conn = psycopg2.connect(user="postgres",
                                     password="postgres",
                                     dbname="CMS",
                                     host='localhost')

    def check_url_available(self, url_list):
        for url in url_list:
            if not url:
                return "Url not found"
            else:
                check = urllib2.urlopen(url)
                if check.code == 200:
                    return "Available"
                else:
                    return "Not available"

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        cursor.execute("insert into cms_urls ( url, title, title_without_url, category, url_available ) values (%s, %s, %s, %s, %s);",
                       [
                           item["url"],
                           item["title"],
                           item["title_without_url"],
                           item["category"],
                           self.check_url_available(item["url"])
                       ])
        self.conn.commit()
        return item
