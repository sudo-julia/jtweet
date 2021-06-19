# -*- coding: utf-8 -*-
"""get api key values from strings or keyfiles"""
from __future__ import annotations
import configparser
import os
import appdirs
from jtweet import NAME, AUTHOR, VERSION


# TODO (jam) would a class store this information more easily?
config_dir: str = appdirs.user_config_dir(NAME, AUTHOR, VERSION)


def get_config(config_file: str) -> dict[str, str]:
    """get options from config file
    return api_api_keys, a list with the consumer key as the first value,
    and consumer secret as the second
    """
    if not os.path.exists(config_file):
        write_config(config_file)

    config = configparser.ConfigParser()
    config.read(config_file)

    config_info: dict[str, dict[str, str]] = {}
    config_info["keys"] = {}
    config_info["locations"] = {}

    keys: configparser.SectionProxy = config["keys"]
    config_info["keys"]["ConsumerKey"] = keys["ConsumerKey"]
    config_info["keys"]["ConsumerSecret"] = keys["ConsumerSecret"]
    config_info["keys"]["AccessTokenKey"] = keys["AccessTokenKey"]
    config_info["keys"]["AccessTokenSecret"] = keys["AccessTokenSecret"]

    locations: configparser.SectionProxy = config["locations"]
    config_info["locations"]["LogLocation"] = locations["LogLocation"]

    for key, value in config_info["keys"].items():
        value = expand_tilde(key)
        if os.path.exists(value):
            config_info["keys"][key] = read_key(value)

    return config_info["keys"]


def write_config(config_file: str):
    """write the config file"""
    if not os.path.exists(config_file):
        os.makedirs(config_dir)
    config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)

    config["KEYS"] = {  # type: ignore -- pass this type checking for the config comment
        "; Value can be the key itself, or the filepath to a file containing it": None,
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

    try:
        with open(config_file, "w") as configfile:
            config.write(configfile)
    # TODO (jam) handle this differently
    except PermissionError as error:
        SystemExit(error)


def expand_tilde(key: str) -> str:
    """expand the tilde to home path"""
    return os.path.expanduser(key)


def read_key(location: str) -> str:
    """get key values from locations"""
    with open(location) as file:
        value: str = file.read().strip()
    return value
