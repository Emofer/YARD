"""
Interpreter module
"""
import logging
import os
import sys
import select
import pickle

from .object_code import *

logger = logging.getLogger(__name__)


class Interpreter:
    """
    The interpreter runs the object code i.e. the Service.
    The interpreter manages a table of variables and use information of the object code to run.

    Example
    >>> interpreter = Interpreter()
    >>> interpreter.load("foo.yo")
    >>> interpreter.run()
    """

    def __init__(self, variables: dict[str:str] = dict(), service: Service = Service(tuple()), pwd: str = '.'):
        if service.steps:
            self.__steps: dict[str:tuple[Command]] = {step.name: step.commands for step in service.steps}
            self.__cur_step: str = service.steps[0].name

        self.__variables: dict[str:str] = variables
        self.__variables["$_last_response"] = ""
        self.__ended = False
        os.chdir(pwd)

    def run(self) -> None:
        """
        Run the object code

        :return: None
        """
        while not self.__ended:
            for command in self.__steps[self.__cur_step]:
                if self.__call_method_by_command_name(command):
                    break

    def load(self, path: str) -> None:
        """
        Load the object code from the given path.

        :param path: Path to the object code
        :return: None
        """
        with open(path, "rb") as file:
            self.__init__(service=pickle.load(file))

    def __visit_var(self, var: str) -> str:
        """
        Visit a variable.

        :param var: the variable name
        :return: the value of the variable
        """
        if var in self.__variables:
            return self.__variables[var]
        logger.error(f"Variable {var} not defined")
        raise KeyError(f"{var} is not defined.")

    def __calc_expr(self, expr: Expression) -> str:
        """
        Calculate the expression.

        :param expr: the expression to calculate
        :return: the value of the expression
        """
        return ''.join([self.__visit_var(term) if term[0] == "$" else term for term in expr.terms])

    def __call_method_by_command_name(self, command: Command):
        """
        Call method by its name. e.g. if command is an instance of Assign(), run __assign()

        :param command: the Command instance
        :return: what the method returns
        """
        method_name = "_" + type(self).__name__ + "__" + type(command).__name__.lower()
        if hasattr(self, method_name) and callable(getattr(self, method_name)):
            return getattr(self, method_name)(command)
        else:
            logger.error(f"No such method: {method_name}")
            raise NameError(f"No such method: {method_name}")

    # methods below are all actions for each command
    def __assign(self, command: Assign):
        """
        Assign the variable. will register it.

        :param command: the assign command
        :return: None
        """
        self.__variables[command.var] = self.__calc_expr(command.expression)

    def __speak(self, command: Speak):
        """
        Speak action, just print.

        :param command: the Speak command
        :return: None
        """
        print(self.__calc_expr(command.to_say))

    def __listen(self, command: Listen):
        """
        Wait the given time for user input. If out of time, the input is "".

        :param command: the listen command
        :return: None
        """
        i, o, e = select.select([sys.stdin], [], [], int(self.__calc_expr(command.time)))
        if i:
            user_input = sys.stdin.readline().strip()
        else:
            user_input = ""
        self.__variables["$_last_response"] = user_input
        self.__variables[command.var] = user_input

    def __branch(self, command: Branch):
        if self.__visit_var("$_last_response") == self.__calc_expr(command.prompt):
            self.__cur_step = command.goto
            return True

    def __silence(self, command: Silence):
        if self.__visit_var("$_last_response") == "":
            self.__cur_step = command.goto
            return True

    def __default(self, command: Default):
        self.__cur_step = command.goto
        return True

    def __end(self, command: End):
        self.__ended = True
        return True

    def __runpy(self, command: Runpy):
        logger.debug(f"running {self.__calc_expr(command.python_code)}")
        exec(self.__calc_expr(command.python_code))

    def __system(self, command: System):
        os.system(self.__calc_expr(command.command_line))
