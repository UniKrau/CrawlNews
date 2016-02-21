#!/usr/bin/python
# -*- coding: utf-8 -*-

# __author__ 'Hao LI'

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from CrawlBBC.items import CrawlbbcItem
import logging
from CrawlBBC.utils.selector import new_prefix

logging.getLogger("NewsSpider")


class NewsSpider(CrawlSpider):
    name = "bbcNews"

    allowed_domains = ["www.bbc.com"]

    start_urls = ["http://www.bbc.com/"]

    rules = (Rule(LinkExtractor(allow=r'/news/[^/]',),

                  callback="parse", process_links="filter_links", follow=True),

             Rule(LinkExtractor(allow=r'/sport/[^/]',),

                  callback="parse", process_links="filter_links", follow=True),

             )

    def parse(self, response):

        URLgroup=LinkExtractor(deny={r'\/privacy', r'\/contact', r'\/iplayer', r'\/help',}).extract_links(response)

        for URL in URLgroup:
            if new_prefix in URL.url:

                yield Request(url=URL.url, callback=self.parse_content)

    def filter_links(self, links):

        filteredLinks = []

        for link in links:
            if link.url.find(new_prefix) < 0:
                filteredLinks.append(link)

    def parse_content(self, response):

        """

        :param response:
        """
        sel = Selector(response)
        items = []
        item = CrawlbbcItem()

        item['news_title'] = response.xpath('/html/head/title/text()').extract()

        item['article_text'] = response.xpath('//p/text()').extract()

        item['article_url'] = response.url.strip()

        item["depth"] = response.meta["depth"]

        items.append(item)

        return items

    def __init__(self):
        pass
