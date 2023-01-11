import pytest
import unittest

from unittest.mock import patch

from services.get import Get
from libs.env import ENV
from libs.db import DB

@pytest.mark.usefixtures("setup_database")
@pytest.mark.usefixtures("clean_database")
class TestGet(unittest.TestCase):

    @patch("services.get.Get.get_paragraph")
    @pytest.mark.run(order=1)
    def test_store_paragraph_success(self, mock_paragraph):
        get_instance = Get()
        paragraphs = [
            'One cannot separate turnovers from endless woods. In modern times a seed is a tulip from the right perspective.',
            'We can assume that any instance of a continent can be construed as a blubber kale. Those tempers are nothing more than deserts.',
            'The sons could be said to resemble napless balls. Some abuzz carols are thought of simply as hydrofoils.',
            'One cannot separate turnovers from endless woods. In modern times a seed is a tulip from the right perspective.'
        ]
        for paragraph in paragraphs:
            mock_paragraph.return_value = paragraph, 200
            response = get_instance.store_paragraph()
            self.assertEqual(response['paragraph'], paragraph)

    @patch("services.get.Get.get_paragraph")
    @pytest.mark.run(order=2)
    def test_store_paragraph_failure(self, mock_paragraph):
        get_instance = Get()
        url = ENV["METAPHORPSUM_URL"].replace('<numberOfParagraphs>', str(Get.PARAGRAPH_CNT)).replace('<numberOfSentences>', str(Get.SENTENCES_CNT))
        error = {'errors':[{'message': f'Failed to fetch the paragraph using url: {url}'}]}
        mock_paragraph.return_value = error, 500
        response, status_code = get_instance.store_paragraph()
        self.assertEqual(response, error)
        self.assertEqual(status_code, 500)

    @patch("services.get.Get.get_paragraph")
    @pytest.mark.run(order=3)
    def test_frequency(self, mock_paragraph):
        expected_words = ['perspective', 'right', 'tulip', 'seed', 'times', 'modern']
        db = DB.get_instance()
        words = list(db[DB.FREQUENCY_CLXN].find({}, {'word': 1, '_id': 0}).sort('count', -1).limit(6))
        self.assertEqual(len(words), 6)
        for word in words:
            self.assertTrue(word['word'] in expected_words)