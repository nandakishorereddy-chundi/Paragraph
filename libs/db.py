import pymongo
import os

from pymongo import MongoClient, TEXT
from libs.env import ENV

class DB:
    '''
    Singleton Class which creates only one instance and returns the instance
    '''
    DATABASE = ENV['DATABASE']

    PARAGRAPH_CLXN = "paragraphs"
    FREQUENCY_CLXN = "frequencies"
    BOOKMARL_CLXN = "bookmarks"

    mongoc = MongoClient(host=ENV['MONGO_SERVER'], port=ENV['MONGO_PORT'])

    __instance__ = None

    def __init__(self):
        if  DB.__instance__ is None:
            self.db = self.mongoc[DB.DATABASE]
            self.db[DB.FREQUENCY_CLXN].create_index('word')
            self.db[DB.FREQUENCY_CLXN].create_index('count')
            self.db[DB.PARAGRAPH_CLXN].create_index([('paragraph', TEXT)], default_language='english')
            DB.__instance__ = self.db

    @staticmethod
    def get_instance():
        if DB.__instance__ is not None:
            return DB.__instance__

        DB()
        return DB.__instance__