class Expression:
    def __init__(self, *terms: str):
        self.terms = terms

    def __str__(self):
        return str(self.terms)

    def __repr__(self):
        return self.__str__()


class Command:
    def __init__(self, name: str, *args: str | Expression):
        self.name = name
        self.args = args

    def __str__(self):
        return str((self.name, self.args))

    def __repr__(self):
        return self.__str__()


class Assign(Command):
    def __init__(self, var: str, expression: Expression):
        super().__init__("assign", var, expression)
        self.var = var
        self.expression = expression


class Speak(Command):
    def __init__(self, to_say: Expression):
        super().__init__("speak", to_say)
        self.to_say = to_say


class Listen(Command):
    def __init__(self, time: Expression, var: str = None):
        super().__init__("listen", time, var)
        self.time = time
        self.var = var


class Branch(Command):
    def __init__(self, prompt: Expression, goto: str):
        super().__init__("branch", prompt, goto)
        self.prompt = prompt
        self.goto = goto


class Silence(Command):
    def __init__(self, goto: str):
        super().__init__("silence", goto)
        self.goto = goto


class Default(Command):
    def __init__(self, goto: str):
        super().__init__("default", goto)
        self.goto = goto


class End(Command):
    def __init__(self):
        super().__init__("exit")


class Runpy(Command):
    def __init__(self, python_code: Expression):
        super().__init__("runpy", python_code)
        self.python_code = python_code


class System(Command):
    def __init__(self, command_line: Expression):
        super().__init__("system", command_line)
        self.command_line = command_line


class Step:
    def __init__(self, name: str, commands: tuple[Command]):
        self.name = name
        self.commands = commands

    def __str__(self):
        return str((self.name, self.commands))

    def __repr__(self):
        return self.__str__()


class Service:
    def __init__(self, steps: tuple[Step]):
        self.steps: tuple[Step] = steps

    def __str__(self):
        return str(self.steps)

    def __repr__(self):
        return self.__str__()
