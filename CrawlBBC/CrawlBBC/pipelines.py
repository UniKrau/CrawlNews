# -*- coding: utf-8 -*-

# __author__ 'Hao LI'

# Define your item pipeline here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import traceback
import logging
import boto3
from CrawlBBC.dbs.mongodb import NewsDB
from pymongo import MongoClient
#from CrawlBBC.settings import IMAGES_STORE
import json

from boto.s3.key import Key


class CrawlbbcPipeline(object):

    # single mongo db

    def process_item(self, item, spider):

        if spider.name != "bbcNews":

            return item

        import json
        json_data = {}
        for t in item['json_data']:
            json_data = json.loads(t)
            if json_data.has_key('itemListElement'):
                # can list for future
                del json_data['itemListElement']
        json_data['text'] = item['text']
        json_data['depth'] = item['depth']
        # dic ={}
        # xx = []
        # for t in item['json_data']:
        #    json_data = json.loads(t)
        #    if json_data.has_key('itemListElement'):
        #        list_data = json_data.get('itemListElement')
        #        print("--------------\n")
        #        dic = list_data[0]
        #        xx.extend([self.make_requests_from_url(dic.get('url')).replace(callback=self.parse)])
        #    if 'author' in json_data.keys():
        #        print (json_data['author'])
        # data = {"news_title": item['news_title'],
        #        "article_url": json_data['url'],
        #        "article_text": item['article_text'],
        #        'update_time': datetime.datetime.utcnow(),  # for comparison
        #        }
        # save to mongo DB
        NewsDB.news.insert(json_data)

        return None

# upload data to S3
#class awspipeline(object):

    #  def process_item(self, item, spider):
       # s3client = boto3.mongoclient(IMAGES_STORE)

       # s3client.put_object(Bucket='haoli', Key='news_title', Body='article_url')

       # return item


class ShardMongodbPipeline(object):
    """
        save the data to shard mongodb.
    """

    HOST = "localhost"
    PORT = 27017
    DB = "NewsDB"
    GridFs_Collection = "news"

    def __init__(self):
        """
            The only async framework that PyMongo fully supports is Gevent.

            Currently there is no great way to use PyMongo in conjunction with Tornado or Twisted. PyMongo provides built-in connection pooling, so some of the benefits of those frameworks can be achieved just by writing multi-threaded code that shares a MongoClient.
        """

        try:
            client = MongoClient(self.HOST, self.PORT)
            self.db = client[self.DB]
        except Exception as e:
            print self.style.ERROR("ERROR(ShardMongodbPipeline): %s"%(str(e),))
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        cls.SERVER = crawler.settings.get('HOST', '10.0.0.7')
        cls.PORT = crawler.settings.getint('PORT', 27017)
        cls.DB = crawler.settings.get('DB', 'NewsDB')
        cls.GridFs_Collection = crawler.settings.get('GridFs_Collection', 'news')
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        if spider.name != "bbcNews":
            return item

        json_data = {}
        for t in item['json_data']:
            json_data = json.loads(t)
        json_data['text'] = item['text']
        json_data['depth'] = item['depth']
        # data = {"news_title": item['news_title'],
        #        "article_url": json_data['url'],
        #        "article_text": item['article_text'],
        #        'update_time': datetime.datetime.utcnow(),  # for comparison
        #        }
        # save to mongo DB
        NewsDB.news.insert(json_data)

        return item
