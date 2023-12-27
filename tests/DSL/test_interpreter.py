from unittest import TestCase

from src import *

class TestInterpreter(TestCase):
    def test_run(self):
        self.interpreter = Interpreter()
        self.interpreter.load("test_run.yo")
        self.interpreter.run()

