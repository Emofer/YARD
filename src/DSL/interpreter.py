class Interpreter:
    """
    The interpreter runs the object code.
    The interpreter manages a table of variables and use all the other information to run a state machine.

    Example
    interpreter = Interpreter()
    interpreter.run(object_code)
    """

    def __init__(self):
        self.variables: dict[str:str] = dict()



