import unittest
import random

from faker import Faker
from json_parser import parse_json, KeyWordList


class TestPraseJSON(unittest.TestCase):

    def test_case_1(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields = ["key1"]
        keywords = ["word2"]

        key_list = KeyWordList()
        parse_json(json_str, key_list, required_fields, keywords)

        self.assertEqual(key_list.list.sort(), keywords.sort())

    def test_case_2(self):
        fake = Faker()

        json = fake.pydict(10, value_types="str")
        json_str = str(json).replace("'", '"')
        
        required_fields = random.sample(list(json.keys()), 5)

        keywords = []
        for key in required_fields:
            keywords.append(str(json[key]))

        key_list = KeyWordList()
        parse_json(json_str, key_list, required_fields, keywords)

        self.assertEqual(key_list.list.sort(), keywords.sort())

    def test_case_3(self):
        fake = Faker()

        json = fake.pydict(10, value_types="str")
        json_str = str(json).replace("'", '"')

        key_list = KeyWordList()
        parse_json(json_str, key_list)

        self.assertEqual(len(key_list.list), 0)
