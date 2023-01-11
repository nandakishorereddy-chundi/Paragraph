import pytest
import unittest

from unittest.mock import patch
from aiounittest import AsyncTestCase

from services.get import Get
from services.dictionary import Dictionary
from libs.env import ENV
from libs.db import DB

@pytest.mark.usefixtures("setup_database")
@pytest.mark.usefixtures("clean_database")
class TestDictionary(AsyncTestCase):
    
    @patch("services.get.Get.get_paragraph")
    @pytest.mark.run(order=9)
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

    @pytest.mark.asyncio
    async def test_get_meaning(self):
        Dictionary.NO_OF_WORDS = 5
        expected_meanings = {
            'perspective': 'A view, vista or outlook.',
            'right': 'Straight, not bent.',
            'tulip': 'A type of flowering plant, genus Tulipa.',
            'seed': 'A fertilized and ripened ovule, containing an embryonic plant.',
            'times': 'The inevitable progression into the future with the passing of present and past events.'
        }
        result = await Dictionary().get_meaning()
        self.assertEqual(result['meanings'], expected_meanings)