import logging
from src import *

config = ConfigLoader(config_path).load()
logging.basicConfig(filename=config["log"]["path"], level=config["log"]["level"], format=log_format)
logger = logging.getLogger(__name__)


def main():
    logger.info(f"Starting with config {config}")
    with open(config["service"]["path"], 'r') as f:
        text = f.read()
    parser = Parser()
    generator = CodeGenerator()
    t = parser.parse(text)
    c = generator.transform(t)
    interpreter = Interpreter(variables=config["service"]["variables"], service=c, pwd=config["pwd"])
    interpreter.run()


if __name__ == "__main__":
    main()
