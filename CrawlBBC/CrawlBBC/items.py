# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlbbcItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    ld_json = scrapy.Field()
    depth = scrapy.Field()

#class AWSItem(scrapy.Item):

    # image_url = scrapy.Field()
