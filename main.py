"""
Main module of the project, including main()
"""
import logging
from src import *


def main():
    """
    Main function of the project. It loads config, generate AST and object codes then run it.

    :return: None
    """
    # load config
    config = ConfigLoader(config_path).load()
    logging.basicConfig(filename=config["log"]["path"], level=config["log"]["level"], format=log_format)
    logger = logging.getLogger(__name__)

    logger.info(logo)
    logger.info(f"Starting with config {config}")
    logger.info(f"reading service file...")
    with open(config["service"]["path"], 'r') as f:
        text = f.read()

    # generate AST and object codes then run
    parser = Parser()
    generator = CodeGenerator()

    logger.info("parsing service file...")
    t = parser.parse(text)

    logger.info("generating object code...")
    c = generator.transform(t)

    interpreter = Interpreter(variables=config["service"]["variables"], service=c, pwd=config["pwd"])
    print(logo)
    logger.info("running...")
    interpreter.run()
    logger.info("done.")


if __name__ == "__main__":
    main()
