# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from FLH.items import FlhItem
import urllib2
class FlSpider(CrawlSpider):
    name = 'F'
    allowed_domains = ['freelancehunt.com']
    start_urls = ['https://freelancehunt.com/freelancers?q=CMS&country=1&city=']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        fl_link = hxs.select("//div[@style='vertical-align: middle; line-height: 26px']/a/@href").extract()
        links=[]
        for link in fl_link:
            links.append('https://freelancehunt.com'+link)
        for url in links:
            yield Request(url, self.parse_items)

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath("//div[@class='snippet-position-container']")
        items=[]
        for titles in titles:
            item = FlhItem()
            item["url"] = titles.select("h4/a/@href").extract()
            if not item["url"]:
                item["url"]=[' ']
                item["title_without_url"] = titles.select("h4/text()").re("\s*\n?(.+)\n")
                item["title"]=' '
            else:
                item["title"] = titles.select("h4/a/text()").re("\s*\n?(.+)\n")
                item["title_without_url"]=' '
                if isinstance(item["url"],list):
                    url_to_request = item["url"][0]
                else:
                    url_to_request =item["url"]
                url_decoded = self.decode_idna(url_to_request)
            yield Request(url_decoded, callback=self.search_cms, dont_filter=True, meta={'item': item})

    def search_cms(self, response):
        cms_dict = {
         'WordPress': 'wp-content',
         'Joomla': 'blablaJoomla'
        }
        cms = 'WordPress'
        item = response.meta['item']
        hxs = HtmlXPathSelector(response)
        body = hxs.xpath('//body').extract_first()
        if cms_dict[cms] in body:
            item["cms"] = cms
        else:
            item["cms"] = ' '
        yield item

    def decode_idna(self, url):
        part = url.split('//')
        if part[1].endswith('/'):
            address = part[1].replace('/','')
        else:
            address = part[1]
        url_decoded = part[0]+'//'+address.encode('idna')
        return url_decoded
