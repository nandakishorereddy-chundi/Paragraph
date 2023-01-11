import asyncio
import aiohttp
import json

from libs.db import DB
from libs.env import ENV
from libs.logger import Logger

class Dictionary:

    NO_OF_WORDS = 10

    async def get_meaning(self):
        self.db = DB.get_instance()
        self.logr = Logger.get_instance()
        
        results = list(self.db[DB.FREQUENCY_CLXN].find({}).sort('count', -1).limit(Dictionary.NO_OF_WORDS))

        urls = [ENV['DICTIONARY_API_BASE_URL'] + result['word'] for result in results]
        
        async with aiohttp.ClientSession() as session:
            meaning = await asyncio.gather(*[self.get_meaning_helper(url, session) for url in urls])

        meanings = {}
        for ix in range(len(results)):
            word = results[ix]['word']
            meanings[word] = meaning[ix]
        return {'meanings': meanings}

    async def get_meaning_helper(self, url, session):
        try:
            async with session.get(url=url, timeout = 2.50) as response:
                try:
                    resp = await response.read()
                    resp = json.loads(resp.decode())
                    if len(resp) == 0 or \
                        len(resp[0]['meanings']) == 0 or \
                        len(resp[0]['meanings'][0]['definitions']) == 0:
                        return 'Meaning for this word is not found'
                    return resp[0]['meanings'][0]['definitions'][0]['definition']
                except Exception as e:
                    self.logr.log_error('Unable to get url {} due to {}.'.format(url, e))
                    return 'Meaning for this word is not found'
        except Exception as e:
            self.logr.log_error(traceback.format_exc())
            return None
