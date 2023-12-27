import pickle

from lark import Transformer, Tree
from lark.visitors import _Leaf_T

from .parser import Parser
from .object_code import *


class CodeGenerator(Transformer):
    """
    CodeGenerator for AST. Read an AST and transform abstract nodes into object code.

    Example

        generator = CodeGenerator()

        generator.transform(tree)
    """

    def service(self, step_blocks):
        """
        Action for service. Lark call this method when a service node is read.
        Its return value will replace the branch in the tree.
        The default retval by lark is Tree(Token('RULE','service'), step_blocks).

        Methods below are actions too, without further elaboration.

        :param step_blocks: list of step_blocks
        :return: tuple of step_blocks
        """
        return Service(tuple(step_blocks))

    def step_block(self, header_body):
        """
        Action for step_block.

        :param header_body: list of [header, body]
        :return: tuple of [header, body]
        """
        header, body = header_body
        return Step(header, body)

    def step_header(self, step_name):
        """
        Action for step_header.

        :param step_name: list of [step_name]
        :return: name of step
        """
        return step_name[0]

    def step_name(self, CNAME):
        """
        Action for step_name.

        :param CNAME: list of [CNAME]
        :return: CNAME
        """
        return CNAME[0]

    def CNAME(self, name):
        """
        Action for CNAME.

        :param name: Token('CNAME','name')
        :return: name[:]
        """
        return name[:]

    def step_body(self, commands):
        """
        Action for step_body.

        :param commands: list of commands
        :return: tuple of commands
        """
        return tuple(commands)

    def command(self, content):
        """
        Action for command.

        :param content:list of one command
        :return: the command itself
        """
        return content[0]

    def assign(self, var_expression):
        """
        Action for assign.

        :param var_expression: list of [var, expression_var]
        :return: tuple of [var, expression_var]
        """
        var, expression = var_expression
        return Assign(var, expression)

    def expression(self, terms):
        """
        Action for expression_var.

        :param terms: list of terms
        :return: tuple of terms
        """
        return Expression(*terms)

    def term(self, val):
        """
        Action for term.

        :param val:  
        :return:
        """
        return val[0]

    def ESCAPED_STRING(self, string):
        return string[1:-1]

    def var(self, CNAME):
        return "$" + CNAME[0]

    def speak(self, expression):
        return Speak(expression[0])

    def listen(self, expression_var):
        time, var = expression_var
        return Listen(time, var)

    def branch(self, expression_step):
        prompt, goto = expression_step
        return Branch(prompt, goto)

    def silence(self, step):
        return Silence(step[0])

    def default(self, step):
        return Default(step[0])

    def end(self, arg):
        return End()

    def runpy(self, expression):
        return Runpy(expression[0])

    def system(self, expression):
        return System(expression[0])

    def transform(self, tree: Tree[_Leaf_T]) -> Service:
        """
        Transform an AST into object code in memory.

        :param tree: AST to transform
        :return: object code, i.e. Service instance
        """
        return super().transform(tree)

    def generate(self, tree: Tree[_Leaf_T], path: str = "a.yo") -> None:
        """
        Generate the object code file for the given AST.

        :param tree: AST
        :param path: path of the object code file
        :return: None
        """
        object_code = self.transform(tree)
        serialized_object = pickle.dumps(object_code)

        with open(path, 'wb') as file:
            file.write(serialized_object)
