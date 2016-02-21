#!/usr/bin/python
# -*- coding: utf-8 -*-

# __author__ 'Hao LI'

from pymongo import MongoClient
import CrawlBBC.dbs.mongodb
import traceback
import logging


SERVER = "10.0.0.7"
PORT = 27017
DB = 'NewsDB'


class QueryDb(object):

    def __init__(self):

        """
            The only async framework that PyMongo fully supports is Gevent.

            Currently there is no great way to use PyMongo in conjunction with Tornado or Twisted.
            PyMongo provides built-in connection pooling, so some of the benefits of those frameworks
            can be achieved just by writing multi-threaded code that shares a MongoClient.
        """

        try:
            client = MongoClient(SERVER, PORT)
            self.db = client[DB]
        except Exception as e:
            logging.info( self.style.ERROR("ERROR(SingleMongodbPipeline): %s"%(str(e),)))
            traceback.print_exc()

    @classmethod
    def from_crawler(cls,crawler):
        cls.SERVER = crawler.setting.get(SERVER, '10.0.0.7')
        cls.PORT = crawler.setting.get(PORT, 27017)
        cls.DB = crawler.setting.get(DB, "NewsDB")
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def query_text(self,text):

        posts = self.db.posts

        posts.find.one("article_text", text)

        return

    def query_title(self, title):

        posts = self.db.posts

        posts.find.one("article_title", title)
