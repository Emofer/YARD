"""
This module contains definition of all the data structure an object code should have.
"""


class Expression:
    """
    Expression is a list of terms, meaning the sum of the terms.

    :param terms: list of terms
    """

    def __init__(self, *terms: str):
        self.terms = terms

    def __str__(self):
        return str(self.terms)

    def __repr__(self):
        return self.__str__()


class Command:
    """
    Command contains a command name and args passed to it.

    :param name: the command name
    :param args: args passed to it
    """

    def __init__(self, name: str, *args: str | Expression):
        self.name = name
        self.args = args

    def __str__(self):
        return str((self.name, self.args))

    def __repr__(self):
        return self.__str__()


class Assign(Command):
    """
    Assign command is $var = expression.

    :param var: the variable to be assigned to
    :param expression: the expression
    """

    def __init__(self, var: str, expression: Expression):
        super().__init__("assign", var, expression)
        self.var = var
        self.expression = expression


class Speak(Command):
    """
    Speak command contains what to say.

    :param to_say: string to be said
    """

    def __init__(self, to_say: Expression):
        super().__init__("speak", to_say)
        self.to_say = to_say


class Listen(Command):
    """
    Listen command contains the time of waiting and where to store the heard string.

    :param time: waiting time
    :param var: var to store the string
    """

    def __init__(self, time: Expression, var: str = None):
        super().__init__("listen", time, var)
        self.time = time
        self.var = var


class Branch(Command):
    """
    Branch command contains when to go to the next branch and what the next branch is

    :param prompt: the string to be checked equal
    :param goto: the next branch
    """

    def __init__(self, prompt: Expression, goto: str):
        super().__init__("branch", prompt, goto)
        self.prompt = prompt
        self.goto = goto


class Silence(Command):
    """
    Silence command is equal to Branch("", goto). i.e. when nothing is heard

    :param goto: the next branch
    """

    def __init__(self, goto: str):
        super().__init__("silence", goto)
        self.goto = goto


class Default(Command):
    """
    when none of prompts matched, goto this

    :param goto: next branch
    """

    def __init__(self, goto: str):
        super().__init__("default", goto)
        self.goto = goto


class End(Command):
    """
    End the session.
    """

    def __init__(self):
        super().__init__("end")


class Runpy(Command):
    """
    Runpy command contains the python code to be executed.

    :param python_code: the python code
    """

    def __init__(self, python_code: Expression):
        super().__init__("runpy", python_code)
        self.python_code = python_code


class System(Command):
    """
    System command contains the command line to run in a shell.

    :param command_line: the command line
    """

    def __init__(self, command_line: Expression):
        super().__init__("system", command_line)
        self.command_line = command_line


class Step:
    """
    Step contains the name of the step and a list of commands in the step.

    :param name: name of the step
    :param commands: list of commands
    """

    def __init__(self, name: str, commands: tuple[Command]):
        self.name = name
        self.commands = commands

    def __str__(self):
        return str((self.name, self.commands))

    def __repr__(self):
        return self.__str__()


class Service:
    """
    A service is a list of steps

    :param steps: list of steps
    """
    def __init__(self, steps: tuple[Step]):
        self.steps: tuple[Step] = steps

    def __str__(self):
        return str(self.steps)

    def __repr__(self):
        return self.__str__()
