import pytest
import unittest

from unittest.mock import patch

from services.get import Get
from services.search import Search
from libs.env import ENV
from libs.db import DB

@pytest.mark.usefixtures("setup_database")
@pytest.mark.usefixtures("clean_database")
class TestSearch(unittest.TestCase):
    
    
    @patch("services.get.Get.get_paragraph")
    @pytest.mark.run(order=4)
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


    @patch("services.search.Search.formatted_data")
    @pytest.mark.run(order=5)
    def test_search_paragraph_and_operator(self, mock_data):
        get_instance = Search()
        mock_data.return_value = (['turnovers', 'tulip', 'perspective'], 'AND')
        response = get_instance.search_paragraph()
        expected_response = [
            {'paragraph': 'One cannot separate turnovers from endless woods. In modern times a seed is a tulip from the right perspective.'},
            {'paragraph': 'One cannot separate turnovers from endless woods. In modern times a seed is a tulip from the right perspective.'}
        ]
        self.assertEqual(len(response['paragraphs']), 2)
        self.assertEqual(response['paragraphs'], expected_response)

    @patch("services.search.Search.formatted_data")
    @pytest.mark.run(order=6)
    def test_search_paragraph_or_operator(self, mock_data):
        get_instance = Search()
        mock_data.return_value = (['turnovers', 'instance', 'resemble'], 'OR')
        response = get_instance.search_paragraph()
        expected_response = [
            {'paragraph': 'One cannot separate turnovers from endless woods. In modern times a seed is a tulip from the right perspective.'},
            {'paragraph': 'We can assume that any instance of a continent can be construed as a blubber kale. Those tempers are nothing more than deserts.'},
            {'paragraph': 'The sons could be said to resemble napless balls. Some abuzz carols are thought of simply as hydrofoils.'},
            {'paragraph': 'One cannot separate turnovers from endless woods. In modern times a seed is a tulip from the right perspective.'},
        ]
        self.assertEqual(len(response['paragraphs']), 4)
        for paragraph in response['paragraphs']:
            self.assertTrue(paragraph in expected_response)

    @patch("services.search.Search.formatted_data")
    @pytest.mark.run(order=7)
    def test_search_paragraph_undefined_operator(self, mock_data):
        get_instance = Search()
        mock_data.return_value = (['turnovers', 'instance', 'resemble'], 'XOR')
        response, status_code = get_instance.search_paragraph()
        self.assertEqual(response, {'errors':[{'message': 'unsupported operator, supported operators are [OR, AND]'}]})
        self.assertEqual(status_code, 422)

    @pytest.mark.run(order=8)
    def test_prepare_query(self):
        get_instance = Search()
        words = ['turnovers', 'hydrofoils']
        query = 'OR'
        query, projection = get_instance.prepare_query(words, query)
        expected_projection = { 'paragraph': 1, '_id': 0 }
        expected_query = { "$text": { "$search": "turnovers hydrofoils" } }
        self.assertEqual(query, expected_query)
        self.assertEqual(projection, expected_projection)