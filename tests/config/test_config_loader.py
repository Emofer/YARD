import os
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import mock_open

from src import *


class TestConfigLoader(TestCase):
    def test_load(self):
        config_file_stub = [
            """pwd: .

log:
  level: INFO
  path: YARD.log

service:
  path: ./services/customer.ys # path of service file, "ys" means "YARD service"
  variables: { }
"""]
        answers = [
            {'log': {'level': 20, 'path': 'YARD.log'}, 'pwd': '.', 'service': {'path': './services/customer.ys',
                                                                               'variables': {}}},
        ]

        for i in range(len(answers)):
            loader = ConfigLoader('/path/to/config/file.yaml')
            with patch('builtins.open', mock_open(read_data=config_file_stub[i])):
                self.assertEqual(loader.load(), answers[i])

    def test_update(self):
        tests = [
            ({'a': 1, 'b': 2}, {'b': 3, 'c': 4}),
            ({'a': 1, 'b': {'c': 2, 'd': 3}}, {'b': {'c': 4, 'e': 5}, 'f': 6}),
            ({}, {'a': 1, 'b': {'c': 2}})
        ]
        answers = [{'a': 1, 'b': 3, 'c': 4}, {'a': 1, 'b': {'c': 4, 'd': 3, 'e': 5}, 'f': 6}, {'a': 1, 'b': {'c': 2}}]
        for i in range(len(answers)):
            self.assertEqual(ConfigLoader.update(*tests[i]), answers[i])
