# -*- coding: utf-8 -*-

# __author__ 'Hao LI'

# Define your item pipeline here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
from CrawlBBC.dbs.mongodb import NewsDB
#from CrawlBBC.settings import IMAGES_STORE
import boto3
from boto.s3.key import Key
import logging


class CrawlbbcPipeline(object):

    # single mongo db

    def process_item(self, item, spider):

        if spider.name != "bbcNews":

            return item

        if not item['news_title']:

            return item

        data = {"news_title": item['news_title'],
                "article_url": item['article_url'],
                "article_text": item['article_text'],
                'update_time': datetime.datetime.utcnow(),  # for comparison
                }
        logging.info("save data ")
        # save to mongo DB
        NewsDB.news.insert(data)

        return None

# upload data to S3
#class awspipeline(object):

    #  def process_item(self, item, spider):
       # s3client = boto3.mongoclient(IMAGES_STORE)

       # s3client.put_object(Bucket='haoli', Key='news_title', Body='article_url')

       # return item
