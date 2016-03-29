# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FlhItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    title_without_url = scrapy.Field()
    category = scrapy.Field()
