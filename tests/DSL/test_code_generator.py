from unittest import TestCase

from lark import Tree
from src import *


class TestCodeGenerator(TestCase):
    def parser_stub(self):
        trees = [
            Tree('service', [
                Tree('step_block', [
                    Tree('step_header', [Tree('step_name', ['MyStep'])]),
                    Tree('step_body', [
                        Tree('command',
                             [Tree('assign',
                                   [Tree('var', ['$var']), Tree('expression', [Tree('term', ['"value"'])])])]),
                        Tree('command', [Tree('speak', [Tree('expression', [Tree('term', ['"Hello, World!"'])])])]),
                    ])
                ]),
            ]),
            Tree('service', [
                Tree('step_block', [
                    Tree('step_header', [Tree('step_name', ['Initialize'])]),
                    Tree('step_body', [
                        Tree('command',
                             [Tree('assign', [Tree('var', ['$counter']), Tree('expression', [Tree('term', ['0'])])])]),
                        Tree('command',
                             [Tree('speak', [Tree('expression', [Tree('term', ['"Initialization complete."'])])])]),
                        Tree('command', [Tree('listen', [Tree('expression', [Tree('term', ['"User input"'])]),
                                                         Tree('var', ['$user_input'])])]),
                    ])
                ]),
                Tree('step_block', [
                    Tree('step_header', [Tree('step_name', ['Loop'])]),
                    Tree('step_body', [
                        Tree('command', [Tree('speak', [
                            Tree('expression', [Tree('term', ['"Loop iteration: "']), Tree('var', ['$counter'])])])]),
                        Tree('command', [Tree('assign', [Tree('var', ['$counter']), Tree('expression',
                                                                                         [Tree('term', ['$counter']),
                                                                                          '+',
                                                                                          Tree('term', ['1'])])])]),
                        Tree('command', [Tree('branch',
                                              [Tree('expression',
                                                    [Tree('term', ['$counter']), '<', Tree('term', ['5'])]),
                                               Tree('step_name', ['Loop'])])]),
                    ])
                ]),
                Tree('step_block', [
                    Tree('step_header', [Tree('step_name', ['Finalize'])]),
                    Tree('step_body', [
                        Tree('command',
                             [Tree('speak', [Tree('expression', [Tree('term', ['"Finalizing process."'])])])]),
                        Tree('command', [Tree('end', [])]),
                    ])
                ]),
            ]),
            Tree('service', [
                Tree('step_block', [
                    Tree('step_header', [Tree('step_name', ['Start'])]),
                    Tree('step_body', [
                        Tree('command', [Tree('speak', [Tree('expression', [Tree('term', ['"Starting..."'])])])]),
                        Tree('command', [Tree('runpy', [Tree('expression', [Tree('term', ['"script.py"'])])])]),
                        Tree('command', [Tree('branch', [Tree('expression', [Tree('term', ['"success"'])]),
                                                         Tree('step_name', ['Success'])])]),
                    ])
                ]),
            ])]
        return trees

    def setUp(self):
        self.trees = self.parser_stub()
        self.generator = CodeGenerator()

    def test_transform(self):
        self.answers = [
            "(('MyStep', (('assign', ('$$var', ('\"value\"',))), ('speak', (('\"Hello, World!\"',),)))),)",
            "(('Initialize', (('assign', ('$$counter', ('0',))), ('speak', (('\"Initialization complete.\"',),)), ('listen', (('\"User input\"',), '$$user_input')))), ('Loop', (('speak', (('\"Loop iteration: \"', '$$counter'),)), ('assign', ('$$counter', ('$counter', '+', '1'))), ('branch', (('$counter', '<', '5'), 'Loop')))), ('Finalize', (('speak', (('\"Finalizing process.\"',),)), ('exit', ()))))",
            "(('Start', (('speak', (('\"Starting...\"',),)), ('runpy', (('\"script.py\"',),)), ('branch', (('\"success\"',), 'Success')))),)",
        ]

        for i in range(len(self.answers)):
            self.assertEqual(self.answers[i], str(self.generator.transform(self.trees[i])))
