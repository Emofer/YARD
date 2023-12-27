import logging
import copy
import yaml
from .constants import default_config_path


class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def load(self):
        with open(default_config_path, 'r') as file:
            default_config: dict = yaml.load(file, Loader=yaml.FullLoader)
        with open(self.config_path, 'r') as file:
            user_config: dict = yaml.load(file, Loader=yaml.FullLoader)
        config = ConfigLoader.update(default_config, user_config)
        config["log"]["level"] = getattr(logging, config["log"]["level"].upper())
        return config

    @staticmethod
    def update(src_dict: dict, target_dict: dict):
        for key, value in target_dict.items():
            if key in src_dict and isinstance(src_dict[key], dict) and isinstance(value, dict):
                src_dict[key] = ConfigLoader.update(src_dict[key], value)
            else:
                src_dict[key] = value
        return src_dict
