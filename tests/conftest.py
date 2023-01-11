import pytest

from pymongo import MongoClient

from libs.db import DB
from libs.env import ENV

DB.DATABASE = 'test_portcast'
DB.mongoc = MongoClient(ENV['MONGO_URI'])
database = DB()
database.db = database.mongoc[DB.DATABASE]

@pytest.fixture(scope="session")
def setup_database(request):
    def fin():
        DB.DATABASE = ENV['DATABASE']
        DB.mongoc = MongoClient(host=ENV['MONGO_SERVER'], port=ENV['MONGO_PORT'])
        database.db = database.mongoc[DB.DATABASE]
    request.addfinalizer(fin)


@pytest.fixture(scope="class")
def clean_database(request):
    clxns = database.db.list_collection_names()
    for clxn in clxns:
        database.db[clxn].delete_many({})