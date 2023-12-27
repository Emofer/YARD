import logging
from DSL.parser import Parser
from DSL.code_generator import CodeGenerator
from DSL.interpreter import Interpreter

logging.basicConfig(
    filename="../YARD.log",
    level=logging.INFO,
    format="[%(asctime)s %(name)s %(levelname)s] %(message)s",
)


def main():
    text = """
    step test1
        $foo = "12"
        $bar = "1"
        speak "hello world"
        listen $foo, $bar // listen for $foo 3 sec
        branch "hi", test2
        silence test3
        default test4
    step test2
        runpy "print('nice to meet you')"
        end
    step test3
        system "ls"
        end
    step test4
        speak "default branch"
        end
    """
    parser = Parser()
    generator = CodeGenerator()
    t = parser.parse(text)
    c = generator.transform(t)
    interpreter = Interpreter(c)
    interpreter.run()


if __name__ == "__main__":
    main()
