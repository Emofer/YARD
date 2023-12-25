from lark import Lark

json_parser = Lark("""
    ?value: dict
         | list
         | ESCAPED_STRING
         | SIGNED_NUMBER
         | "true" | "false" | "null"
        
    list : "[" [value ("," value)*] "]"
        
    dict : "{" [pair ("," pair)*] "}"
    pair : ESCAPED_STRING ":" value
        
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
""", start="value")

if __name__ == "__main__":
    text = '{"key": ["item0", "item1", 3.14, true]}'
    t = json_parser.parse(text)
    print(t.pretty())