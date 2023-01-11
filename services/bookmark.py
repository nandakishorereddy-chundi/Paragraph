from flask import request

from libs.db import DB
from libs.logger import Logger

class Bookmark:

    def __init__(self):
        self.db = DB.get_instance()
        self.logr = Logger.get_instance()

    def save_bookmark(self):
        data = request.get_json()
        paragraph_id = data.get('paragraph_id')
        user_id = data.get('user_id')
        self.db[DB.BOOKMARL_CLXN].insert_one({'_userId': user_id, 'paragraph_id', paragraph_id})

    def get_bookmark(self):
        args = request.args 
        user_id = args.get('user_id')
        paragraph_ids = list(self.db[DB.BOOKMARL_CLXN].find({'_userId': user_id}), {'paragraph_id': 1, '_id': 0})
        paragraphs = self.db[DB.PARAGRAPH_CLXN].find({'_id': {'$in': paragraph_ids}})
        return paragraphs

    def bookmark_paragraph(self):
        if request.method == 'POST':
            try:
                self.save_bookmark()
                return {'status': 'success'}, 200
            except Exception as e:
                self.logr.log_error('Unable to save the bookmark, e: {}'.format(e.__class__))
        
        if request.method == 'GET':
            try:
                paragraphs = self.get_bookmark()
                return {'bookmarks': paragraphs}
            except Exception as e:
                self.logr.log_error('Unable to get the bookmarks, e: {}'.format(e.__class__))
