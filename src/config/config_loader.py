"""
Config Loader Module
"""
import logging
import yaml
from .constants import default_config_path


class ConfigLoader:
    """
    Config Loader for yaml config files. Update the default config using user config.

    :param config_path: the config file path
    """

    def __init__(self, config_path: str):
        self.config_path = config_path

    def load(self) -> dict:
        """
        Load config file, update the default config using user config. The default config contains default values.

        :return: config in dict form
        """
        with open(default_config_path, 'r') as file:
            default_config: dict = yaml.load(file, Loader=yaml.FullLoader)
        with open(self.config_path, 'r') as file:
            user_config: dict = yaml.load(file, Loader=yaml.FullLoader)
        config = ConfigLoader.update(default_config, user_config)

        # e.g. turn INFO to logging.INFO
        config["log"]["level"] = getattr(logging, config["log"]["level"].upper())
        return config

    @staticmethod
    def update(src_dict: dict, target_dict: dict):
        """
        update the src dict with target dict. No like the builtin dict().update, this will update recursively.

        :param src_dict: src dict
        :param target_dict: target dict
        :return: updated dict
        """
        for key, value in target_dict.items():
            if key in src_dict and isinstance(src_dict[key], dict) and isinstance(value, dict):
                src_dict[key] = ConfigLoader.update(src_dict[key], value)
            else:
                src_dict[key] = value
        return src_dict
