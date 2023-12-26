from lark import Lark


class Parser(Lark):
    """
    Lark parser for DSL. Used to parse a DSL script and generate an AST

    Example
    my_parser = Parser()
    tree = my_parser.parse("step foo")
    print(tree.pretty())
    """

    def __init__(self):
        super().__init__("""
            service     : step_block*
            step_block  : step_header step_body
            step_header : "step" step_name
            step_name   : CNAME
            step_body   : command*
            command     : assign | speak | listen | branch | silence | default | exit | runpy | system
            assign      : var "=" expression
            expression  : term ("+" term)*
            term        : var | ESCAPED_STRING
            var         : "$" CNAME
            speak       : "speak" expression
            listen      : "listen" expression ["," var]
            branch      : "branch" expression "," step_name
            silence     : "silence" step_name
            default     : "default" step_name
            exit        : "exit"
            runpy       : "runpy" expression
            system      : "system" expression    
            
            %import common (ESCAPED_STRING, WS, CNAME, C_COMMENT, CPP_COMMENT)
            %ignore WS
            %ignore C_COMMENT
            %ignore CPP_COMMENT
        """, start="service", parser="lalr")


if __name__ == "__main__":
    text = """
    step test1
        $foo = "1" + "2" + "3"
        $bar = "1"
        speak "hello world"
        listen $foo + "3", $bar // listen for $foo + 3 sec
        branch "hi", test2
        silence test3
        default test4
    step test2
        runpy "print(123)"
        exit
    step test3
        system "ls"
        exit
    step test4
    """
    t = Parser().parse(text)
    print(t)
    print(t.pretty())
