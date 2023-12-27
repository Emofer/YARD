from lark import Lark, Tree, Token
from ..config.constants import EBNF


class Parser(Lark):
    """
    Lark parser for DSL. Used to parse a DSL script and generate an AST

    Example
    my_parser = Parser()
    tree = my_parser.parse("step foo")
    print(tree.pretty())
    """

    def __init__(self):
        super().__init__(EBNF, start=EBNF.split()[0], parser="lalr")

    def parse(self, text: str, **kwargs) -> Tree[Token]:
        """
        s

        :param text:
        :param kwargs:
        :return:
        """
        return super().parse(text, **kwargs)

    def pretty_print(self, ast):
        print(ast.pretty())
        return ast.pretty()
