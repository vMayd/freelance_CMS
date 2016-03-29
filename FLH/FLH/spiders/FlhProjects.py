from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from FLH.items import FlhItem
import re

class FlSpider(CrawlSpider):
      name = 'FreelanceProjects'
      allowed_domains = ['freelancehunt.com']
      start_urls = ['https://freelancehunt.com/freelancers?q=CMS&country=1&city=']



      def parse (self,response):
         hxs = HtmlXPathSelector(response)
         fl_link = HtmlXPathSelector(response).select("//div[@style='vertical-align: middle; line-height: 26px']/a/@href").extract()
         links=[]
         for link in fl_link:
            links.append('https://freelancehunt.com'+link)
         for index,l in enumerate(links):
            if links:
                yield Request(links[index],self.parse_items)
      def parse_items(self,response):
         hxs = HtmlXPathSelector(response)
         titles = hxs.xpath("//div[@class='snippet-position-container']")
         items=[]
         for titles in titles:
            item = FlhItem()
            item["title"] = titles.select("h4/a/text()").re("\s*\n?(.+)\n")
            item["url"] = titles.select("h4/a/@href").extract()
            if not item["url"]:
                 item["title_without_url"] = titles.select("h4/text()").re("\s*\n?(.+)\n")
            else:
                item["title_without_url"] = None
            item["category"] = titles. select("div[@class='smaller text-muted']/text()").extract()
            items.append(item)
         for item in items:
            yield item
