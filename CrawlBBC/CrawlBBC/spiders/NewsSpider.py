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

    rules = [(Rule(LinkExtractor(allow=r'/news/',), callback="parse", follow=True)),
            (Rule(LinkExtractor(deny=r'/iplayer/[^/]',), callback="parse", follow=False)),
            (Rule(LinkExtractor(deny=r'/weather/[^/]',), callback="parse", follow=False)),
            (Rule(LinkExtractor(deny=r'/http://www.bbc.co.uk/radio/[^/]',), callback="parse", follow=False)),
            (Rule(LinkExtractor(deny=r'/privacy[^/]',), callback="parse", follow=False)),
            (Rule(LinkExtractor(deny=r'/help[^/]',), callback="parse", follow=False)),
             ]

    def parse(self, response):

        # '//a/@href'
        newurls = response.xpath('//div[@id="page"]//section[starts-with(@class,"module")]//'
                                 'div[starts-with(@class, "module__content")]//'
                                 'ul[starts-with(@class, "media-list")]//a/@href'
                                 ).extract()
        items = []
        validurls = []
        for url in newurls:
                url = url.replace("#", " ").strip()
                if new_prefix in url:
                    validurls.append(url)
                elif "http" not in url:
                    url = new_prefix+url
                    validurls.append(url)

        validurls = list(set(validurls))

        items.extend([self.make_requests_from_url(url).replace(callback=self.parse) for url in validurls])

        for URL in validurls:
            yield Request(url=URL, callback=self.parse_content)

    def parse_content(self, response):

        """

        :param response:
        """

        items = []
        item = CrawlbbcItem()
        # '//p/text()'
        item['title'] = response.xpath('/html/head/title/text()').extract()
        item['text'] = response.xpath('//p/text()').extract()
        item["depth"] = response.meta["depth"]
        item['ld_json'] = response.xpath('//script[@type="application/ld+json"]/text()').extract()
        item['abs_url'] = response.url.strip()
        items.append(item)

        return items

    def __init__(self):
        pass
