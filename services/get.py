import requests

from pymongo import UpdateOne

from libs.env import ENV
from libs.db import DB
from libs.logger import Logger
from libs.util import cleanse_text

class Get:

    PARAGRAPH_CNT = 1
    SENTENCES_CNT = 50

    def __init__(self):
        self.db = DB.get_instance()
        self.logr = Logger.get_instance()

    def get_paragraph(self):
        url = ENV["METAPHORPSUM_URL"].replace('<numberOfParagraphs>', str(Get.PARAGRAPH_CNT)).replace('<numberOfSentences>', str(Get.SENTENCES_CNT))
        response = requests.get(url, timeout = 2.50)
        if response.status_code != 200:
            return {'errors':[{'message': f'Failed to fetch the paragraph using url: {url}'}]}, response.status_code
        return response.text, 200

    def update_frequencies(self, text):
        words = cleanse_text(text)
        to_update = {}
        for word in words:
            if word in to_update:
                to_update[word] += 1
            else:
                to_update[word] = 1
        updates = []
        for word in words:
            updates.append(UpdateOne({"word": word}, {'$inc': {'count': to_update[word]}}, upsert = True))

        self.db[DB.PARAGRAPH_CLXN].insert_one({"paragraph": text})
        self.db[DB.FREQUENCY_CLXN].bulk_write(updates, ordered = False)

    def store_paragraph(self):
        response, status_code = self.get_paragraph()
        if status_code != 200:
            return response, status_code
        
        text = response

        try:
            self.update_frequencies(text)
        except Exception as e:
            self.logr.log_error('Unable to update the frequencies, error = {}'.format(e))

        return {
            'paragraph': text
        }