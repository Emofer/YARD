"""
Parser module
"""
from lark import Lark, Tree, Token
from ..config.constants import EBNF


class Parser(Lark):
    """
    Lark parser for DSL. Used to parse a DSL script and generate an AST

    Example

    >>> my_parser = Parser()
    >>> tree = my_parser.parse("step foo")
    >>> my_parser.pretty_print(tree)
    """

    def __init__(self):
        super().__init__(EBNF, start=EBNF.split()[0], parser="lalr")

    def parse(self, text: str, **kwargs) -> Tree[Token]:
        """
        Parse a DSL text and generate an AST

        :param text: the DSL text
        :param kwargs: other keyword arguments passed to lark parser
        :return: AST
        """
        return super().parse(text, **kwargs)

    def pretty_print(self, ast):
        """
        Pretty print the given AST

        :param ast: AST
        :return: the pretty printed AST str
        """
        print(ast.pretty())
        return ast.pretty()
