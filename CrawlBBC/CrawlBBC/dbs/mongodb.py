#!/usr/bin/python
# -*- coding: utf-8 -*-

# __author__ 'Hao LI'


import pymongo
import random

HOST = "10.0.0.7"
PORT = 27017
client = pymongo.MongoClient(HOST, PORT)
NewsDB = client.NewsDB


class distributeMongoDB:


    def __init__(self):
        pass