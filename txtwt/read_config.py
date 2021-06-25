# -*- coding: utf-8 -*-
"""get api key values from strings or keyfiles"""
from __future__ import annotations
import configparser
import os
import appdirs
from txtwt import NAME, AUTHOR, VERSION


class Config:
    """config file manager"""

    def __init__(self, config_dir: str = None, config_file: str = None):
        """initialize the class pointing at a config location"""
        self.config_dir = config_dir or appdirs.user_config_dir(NAME, AUTHOR, VERSION)
        self.config_file = config_file or f"{self.config_dir}/config.ini"

    def read_config(self) -> dict[str, dict[str, str]]:
        """get options from config file
        return api_api_keys, a list with the consumer key as the first value,
        and consumer secret as the second
        """
        try:
            if not os.path.exists(self.config_file):
                self.write_config()
        except PermissionError as error:
            raise NotImplementedError from error

        config = configparser.ConfigParser()
        config.read(self.config_file)

        config_info: dict[str, dict[str, str]] = {}
        config_info["keys"] = {}
        config_info["locations"] = {}

        keys: configparser.SectionProxy = config["KEYS"]
        config_info["keys"]["ConsumerKey"] = keys["ConsumerKey"]
        config_info["keys"]["ConsumerSecret"] = keys["ConsumerSecret"]
        config_info["keys"]["AccessTokenKey"] = keys["AccessTokenKey"]
        config_info["keys"]["AccessTokenSecret"] = keys["AccessTokenSecret"]

        locations: configparser.SectionProxy = config["LOCATIONS"]
        config_info["locations"]["TweetDir"] = locations["TweetDir"]
        config_info["locations"]["LogLocation"] = locations["LogLocation"]

        for key, value in config_info["keys"].items():
            value = expand_tilde(key)
            if os.path.exists(value):
                config_info["keys"][key] = read_key(value)

        return config_info

    def write_config(self):
        """write the config file"""
        try:
            if not os.path.exists(self.config_file):
                os.makedirs(self.config_dir)
            config: configparser.ConfigParser = configparser.ConfigParser(
                allow_no_value=True
            )
        except PermissionError as error:
            raise NotImplementedError from error

        config["KEYS"] = {  # type: ignore
            "; Value can be the key itself or a filepath to a file containing it": None,
            "ConsumerKey": "",
            "ConsumerSecret": "",
            "AccessTokenKey": "",
            "AccessTokenSecret": "",
        }

        config["LOCATIONS"] = {  # type: ignore
            f"; TweetDir is the location that {NAME} will watch for new tweets.": None,
            "TweetDir": appdirs.user_data_dir(NAME),
            "; Location of the logfile": None,
            "LogLocation": appdirs.user_log_dir(NAME),
        }

        with open(self.config_file, "w") as configfile:
            config.write(configfile)


def expand_tilde(key: str) -> str:
    """expand the tilde to home path"""
    return os.path.expanduser(key)


def read_key(location: str) -> str:
    """get key values from locations"""
    with open(location) as file:
        value: str = file.read().strip()
    return value
