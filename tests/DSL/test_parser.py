from unittest import TestCase

from lark import Tree, Token
from src import *


class TestParser(TestCase):
    def test_parse(self):
        texts = [
            """
            step test1
                $foo = "1"
                $bar = "1"
                speak "hello world"
                listen $foo + "0", $bar // listen for $foo + 3 sec
                branch "hi", test2
                silence test3
                default test4
            step test2
                runpy "print(123)"
                end
            step test3
                system "ls"
                end
            step test4
            """,
            """
            step Initialize
                speak "Welcome to the system initialization process."
                $counter = "0"
                listen "5", $initial_value
            
            step Loop
                branch $counter, Loop
                speak "Loop iteration: " + $counter
                $counter = $counter + "1"
            
            step Finalize
                speak "Finalizing the process."
            """
        ]
        answers = [
            Tree(Token('RULE', 'service'), [Tree(Token('RULE', 'step_block'), [
                Tree(Token('RULE', 'step_header'), [Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test1')])]),
                Tree(Token('RULE', 'step_body'), [Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'assign'), [
                    Tree(Token('RULE', 'var'), [Token('CNAME', 'foo')]), Tree(Token('RULE', 'expression'), [
                        Tree(Token('RULE', 'term'), [Token('ESCAPED_STRING', '\"1\"')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'assign'), [
                                                      Tree(Token('RULE', 'var'), [Token('CNAME', 'bar')]),
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '\"1\"')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'speak'), [
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '\"hello world\"')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'listen'), [
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Tree(Token('RULE', 'var'), [Token('CNAME', 'foo')])]),
                                                                                         Tree(Token('RULE', 'term'), [
                                                                                             Token('ESCAPED_STRING',
                                                                                                   '\"0\"')])]),
                                                      Tree(Token('RULE', 'var'), [Token('CNAME', 'bar')])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'branch'), [
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '\"hi\"')])]),
                                                      Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test2')])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'silence'), [
                                                      Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test3')])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'default'), [
                                                      Tree(Token('RULE', 'step_name'),
                                                           [Token('CNAME', 'test4')])])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test2')])]),
                                                                               Tree(Token('RULE', 'step_body'), [
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'runpy'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Token(
                                                                                                             'ESCAPED_STRING',
                                                                                                             '\"print(123)\"')])])])]),
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'end'),
                                                                                            [])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test3')])]),
                                                                               Tree(Token('RULE', 'step_body'), [
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'system'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Token(
                                                                                                             'ESCAPED_STRING',
                                                                                                             '\"ls\"')])])])]),
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'end'),
                                                                                            [])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test4')])]),
                                                                               Tree(Token('RULE', 'step_body'), [])])]),
            Tree(Token('RULE', 'service'), [Tree(Token('RULE', 'step_block'), [
                Tree(Token('RULE', 'step_header'), [Tree(Token('RULE', 'step_name'), [Token('CNAME', 'Initialize')])]),
                Tree(Token('RULE', 'step_body'), [Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'speak'), [
                    Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                        Token('ESCAPED_STRING', '"Welcome to the system initialization process."')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'assign'), [
                                                      Tree(Token('RULE', 'var'), [Token('CNAME', 'counter')]),
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '"0"')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'listen'), [
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '"5"')])]), Tree(Token('RULE', 'var'),
                                                                                                   [Token('CNAME',
                                                                                                          'initial_value')])])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'Loop')])]),
                                                                               Tree(Token('RULE', 'step_body'), [
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'branch'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Tree(Token(
                                                                                                             'RULE',
                                                                                                             'var'), [
                                                                                                             Token(
                                                                                                                 'CNAME',
                                                                                                                 'counter')])])]),
                                                                                           Tree(Token('RULE',
                                                                                                      'step_name'), [
                                                                                                    Token('CNAME',
                                                                                                          'Loop')])])]),
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'speak'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Token(
                                                                                                             'ESCAPED_STRING',
                                                                                                             '"Loop iteration: "')]),
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Tree(Token(
                                                                                                             'RULE',
                                                                                                             'var'), [
                                                                                                             Token(
                                                                                                                 'CNAME',
                                                                                                                 'counter')])])])])]),
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'assign'), [
                                                                                           Tree(Token('RULE', 'var'), [
                                                                                               Token('CNAME',
                                                                                                     'counter')]), Tree(
                                                                                               Token('RULE',
                                                                                                     'expression'), [
                                                                                                   Tree(Token('RULE',
                                                                                                              'term'), [
                                                                                                            Tree(Token(
                                                                                                                'RULE',
                                                                                                                'var'),
                                                                                                                [Token(
                                                                                                                    'CNAME',
                                                                                                                    'counter')])]),
                                                                                                   Tree(Token('RULE',
                                                                                                              'term'), [
                                                                                                            Token(
                                                                                                                'ESCAPED_STRING',
                                                                                                                '"1"')])])])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'Finalize')])]),
                                                                               Tree(Token('RULE', 'step_body'), [
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'speak'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Token(
                                                                                                             'ESCAPED_STRING',
                                                                                                             '"Finalizing the process."')])])])])])])])
        ]
        for i in range(len(answers)):
            self.assertEqual(Parser().parse(texts[i]), answers[i])

    def test_pretty_print(self):
        trees = [
            Tree(Token('RULE', 'service'), [Tree(Token('RULE', 'step_block'), [
                Tree(Token('RULE', 'step_header'), [Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test1')])]),
                Tree(Token('RULE', 'step_body'), [Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'assign'), [
                    Tree(Token('RULE', 'var'), [Token('CNAME', 'foo')]), Tree(Token('RULE', 'expression'), [
                        Tree(Token('RULE', 'term'), [Token('ESCAPED_STRING', '\"1\"')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'assign'), [
                                                      Tree(Token('RULE', 'var'), [Token('CNAME', 'bar')]),
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '\"1\"')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'speak'), [
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '\"hello world\"')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'listen'), [
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Tree(Token('RULE', 'var'), [Token('CNAME', 'foo')])]),
                                                                                         Tree(Token('RULE', 'term'), [
                                                                                             Token('ESCAPED_STRING',
                                                                                                   '\"0\"')])]),
                                                      Tree(Token('RULE', 'var'), [Token('CNAME', 'bar')])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'branch'), [
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '\"hi\"')])]),
                                                      Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test2')])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'silence'), [
                                                      Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test3')])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'default'), [
                                                      Tree(Token('RULE', 'step_name'),
                                                           [Token('CNAME', 'test4')])])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test2')])]),
                                                                               Tree(Token('RULE', 'step_body'), [
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'runpy'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Token(
                                                                                                             'ESCAPED_STRING',
                                                                                                             '\"print(123)\"')])])])]),
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'end'),
                                                                                            [])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test3')])]),
                                                                               Tree(Token('RULE', 'step_body'), [
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'system'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Token(
                                                                                                             'ESCAPED_STRING',
                                                                                                             '\"ls\"')])])])]),
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'end'),
                                                                                            [])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'test4')])]),
                                                                               Tree(Token('RULE', 'step_body'), [])])]),
            Tree(Token('RULE', 'service'), [Tree(Token('RULE', 'step_block'), [
                Tree(Token('RULE', 'step_header'), [Tree(Token('RULE', 'step_name'), [Token('CNAME', 'Initialize')])]),
                Tree(Token('RULE', 'step_body'), [Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'speak'), [
                    Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                        Token('ESCAPED_STRING', '"Welcome to the system initialization process."')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'assign'), [
                                                      Tree(Token('RULE', 'var'), [Token('CNAME', 'counter')]),
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '"0"')])])])]),
                                                  Tree(Token('RULE', 'command'), [Tree(Token('RULE', 'listen'), [
                                                      Tree(Token('RULE', 'expression'), [Tree(Token('RULE', 'term'), [
                                                          Token('ESCAPED_STRING', '"5"')])]), Tree(Token('RULE', 'var'),
                                                                                                   [Token('CNAME',
                                                                                                          'initial_value')])])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'Loop')])]),
                                                                               Tree(Token('RULE', 'step_body'), [
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'branch'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Tree(Token(
                                                                                                             'RULE',
                                                                                                             'var'), [
                                                                                                             Token(
                                                                                                                 'CNAME',
                                                                                                                 'counter')])])]),
                                                                                           Tree(Token('RULE',
                                                                                                      'step_name'), [
                                                                                                    Token('CNAME',
                                                                                                          'Loop')])])]),
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'speak'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Token(
                                                                                                             'ESCAPED_STRING',
                                                                                                             '"Loop iteration: "')]),
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Tree(Token(
                                                                                                             'RULE',
                                                                                                             'var'), [
                                                                                                             Token(
                                                                                                                 'CNAME',
                                                                                                                 'counter')])])])])]),
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'assign'), [
                                                                                           Tree(Token('RULE', 'var'), [
                                                                                               Token('CNAME',
                                                                                                     'counter')]), Tree(
                                                                                               Token('RULE',
                                                                                                     'expression'), [
                                                                                                   Tree(Token('RULE',
                                                                                                              'term'), [
                                                                                                            Tree(Token(
                                                                                                                'RULE',
                                                                                                                'var'),
                                                                                                                [Token(
                                                                                                                    'CNAME',
                                                                                                                    'counter')])]),
                                                                                                   Tree(Token('RULE',
                                                                                                              'term'), [
                                                                                                            Token(
                                                                                                                'ESCAPED_STRING',
                                                                                                                '"1"')])])])])])]),
                                            Tree(Token('RULE', 'step_block'), [Tree(Token('RULE', 'step_header'), [
                                                Tree(Token('RULE', 'step_name'), [Token('CNAME', 'Finalize')])]),
                                                                               Tree(Token('RULE', 'step_body'), [
                                                                                   Tree(Token('RULE', 'command'), [
                                                                                       Tree(Token('RULE', 'speak'), [
                                                                                           Tree(Token('RULE',
                                                                                                      'expression'), [
                                                                                                    Tree(Token('RULE',
                                                                                                               'term'),
                                                                                                         [Token(
                                                                                                             'ESCAPED_STRING',
                                                                                                             '"Finalizing the process."')])])])])])])])
        ]
        answers = [
            """service
  step_block
    step_header
      step_name	test1
    step_body
      command
        assign
          var	foo
          expression
            term	"1"
      command
        assign
          var	bar
          expression
            term	"1"
      command
        speak
          expression
            term	"hello world"
      command
        listen
          expression
            term
              var	foo
            term	"0"
          var	bar
      command
        branch
          expression
            term	"hi"
          step_name	test2
      command
        silence
          step_name	test3
      command
        default
          step_name	test4
  step_block
    step_header
      step_name	test2
    step_body
      command
        runpy
          expression
            term	"print(123)"
      command
        end
  step_block
    step_header
      step_name	test3
    step_body
      command
        system
          expression
            term	"ls"
      command
        end
  step_block
    step_header
      step_name	test4
    step_body
""",
            """service
  step_block
    step_header
      step_name	Initialize
    step_body
      command
        speak
          expression
            term	"Welcome to the system initialization process."
      command
        assign
          var	counter
          expression
            term	"0"
      command
        listen
          expression
            term	"5"
          var	initial_value
  step_block
    step_header
      step_name	Loop
    step_body
      command
        branch
          expression
            term
              var	counter
          step_name	Loop
      command
        speak
          expression
            term	"Loop iteration: "
            term
              var	counter
      command
        assign
          var	counter
          expression
            term
              var	counter
            term	"1"
  step_block
    step_header
      step_name	Finalize
    step_body
      command
        speak
          expression
            term	"Finalizing the process."
"""
        ]
        for i in range(len(answers)):
            self.assertEqual(Parser().pretty_print(trees[i]), answers[i])
