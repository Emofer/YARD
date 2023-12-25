from lark import Transformer
from . import parser


class MyTransformer(Transformer):
    def list(self, items):
        return list(items)

    def pair(self, key_value):
        k, v = key_value
        return k, v

    def dict(self, items):
        return dict(items)

    def ESCAPED_STRING(self, s):
        return s[1: -1]

    def SIGNED_NUMBER(self, n):
        return float(n)

if __name__ == "__main__":
    text = '{"key": ["item0", "item1", 3.14,true]}'
    t = parser.json_parser.parse(text)
    f = MyTransformer().transform(t)
    print(f)
