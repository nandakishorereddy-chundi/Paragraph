from flask import request
from libs.db import DB

class Search:

    def formatted_data(self):
        data = request.get_json()
        words = [word.strip() for word in data.get('words', '').split(',')]
        operator = data.get('operator')
        return words, operator

    def search_paragraph(self):
        words, operator = self.formatted_data()
        query, projection = self.prepare_query(words, operator)
        if query is None:
            return {'errors':[{'message': 'unsupported operator, supported operators are [OR, AND]'}]}, 422

        self.db = DB.get_instance()

        results = list(self.db[DB.PARAGRAPH_CLXN].find(query, projection))
        return {"paragraphs": results}

    def prepare_query(self, words, operator):
        if operator.lower() == 'or':
            query, projection = { "$text": { "$search": " ".join(f'{w}' for w in words) } }, { 'paragraph': 1, '_id': 0 }
        elif operator.lower() == 'and':
            query, projection =  { "$text": { "$search": " ".join(f'"{w}"' for w in words) } }, { 'paragraph': 1, '_id': 0 }
        else:
            query, projection = None, None
        return query, projection



# {$text: {$search: "word1 word2 word3"}}
# {$text: {$search: "\"word1\"  \"word2\"  \"word3\""}}
