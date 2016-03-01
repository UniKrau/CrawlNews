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
            self.posts = self.db.news

        except Exception as e:
            logging.info( self.style.ERROR("ERROR(SingleMongodbPipeline): %s"%(str(e),)))
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        cls.SERVER = crawler.setting.get(SERVER, '10.0.0.7')
        cls.PORT = crawler.setting.get(PORT, 27017)
        cls.DB = crawler.setting.get(DB, "NewsDB")
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def query_text(self, text):

        try:
            if text not in None:
                return self.posts.find({"article_text": text})
        except Exception as e:
            logging.error(" headline is null")
            traceback.print_exc()

    def query_title(self, title):
        if title not in None:
            return self.posts.find({"article_title": title})

    def query_headline(self, headline):

        try:
            if headline is not None:
                return self.posts.find({"headline": headline})
        except Exception as e:
            logging.error(" headline is null")
            traceback.print_exc()

    # logic or query
    def query_or(self, headline, author):
        if headline is None or author is None:
            return " "
        else:
            return self.posts.find({"$or": [{"headline": headline}, {"author": author}]})

    # Single field indexes
    #def createsingleindexes(self):
    #    self.posts.create_index()

    # Compound indexes

    # Multikey indexes

    # Text indexes

    # db.products.find( { description: { $regex: /^S/, $options: 'm' } } )

    def text_match_query(self, context):

        if context is not None:

            return self.posts.find({"text": {"$regex": context}})

if __name__ == '__main__':

    query = QueryDb()

    result = query.query_headline("Oscars 2016: Leonardo DiCaprio finally wins Academy Award")

    for r in result:
        if 'text' in r:
            print ""

    text = query.text_match_query(" today even more")

    for t in text:
        print t.get('text')