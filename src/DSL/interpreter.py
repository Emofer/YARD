import logging
import os
import select
import sys

from DSL.object_code import *

logger = logging.getLogger(__name__)


class Interpreter:
    """
    The interpreter runs the object code i.e. the Service.
    The interpreter manages a table of variables and use all the other information to run a state machine.

    Example
    interpreter = Interpreter()
    interpreter.run(object_code)
    """

    def __init__(self, service: Service):
        if not service:
            logger.error("Service not provided")
            raise ValueError("Servie cannot be empty")
        self.__steps: dict[str:tuple[Command]] = {step.name: step.commands for step in service.steps}
        self.__variables: dict[str:str] = dict()
        self.__cur_step: str = service.steps[0].name
        self.__variables["$_last_response"] = ""

    def run(self):
        while True:
            for command in self.__steps[self.__cur_step]:
                if self.__run_command_by_name(command):
                    break

    def __visit_var(self, var: str) -> str:
        if var in self.__variables:
            return self.__variables[var]
        logger.error(f"Variable {var} not defined")
        raise KeyError(var + "is not defined.")

    def __calc_expr(self, expr: Expression) -> str:
        return ''.join([self.__visit_var(term) if term[0] == "$" else term for term in expr.terms])

    def __run_command_by_name(self, command):
        method_name = "_" + type(self).__name__ + "__" + type(command).__name__.lower()
        if hasattr(self, method_name) and callable(getattr(self, method_name)):
            return getattr(self, method_name)(command)
        else:
            logger.error(f"No such method: {method_name}")
            raise NameError(f"No such method: {method_name}")

    def __assign(self, command: Assign):
        self.__variables[command.var] = self.__calc_expr(command.expression)

    def __speak(self, command: Speak):
        print(self.__calc_expr(command.to_say))

    def __listen(self, command: Listen):
        i, o, e = select.select([sys.stdin], [], [], int(self.__calc_expr(command.time)))
        if i:
            user_input = sys.stdin.readline().strip()
        else:
            user_input = ""
        self.__variables["$_last_response"] = user_input

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
        exit(0)

    def __runpy(self, command: Runpy):
        exec(self.__calc_expr(command.python_code))

    def __system(self, command: System):
        os.system(self.__calc_expr(command.command_line))


if __name__ == "__main__":
    interpreter = Interpreter(Service((Step("step1", ((Speak(Expression("123"))),)),)))
    interpreter.run()
