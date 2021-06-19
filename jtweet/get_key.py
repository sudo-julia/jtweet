# -*- coding: utf-8 -*-
"""get api key values from strings or keyfiles"""
from __future__ import annotations
import configparser
from pathlib import Path
from appdirs import user_config_dir
from jtweet import NAME, AUTHOR, VERSION


config_dir: str = user_config_dir(NAME, AUTHOR, VERSION)


def get_config(config_file: str) -> dict[str, str]:
    """get options from config file
    return api_api_keys, a list with the consumer key as the first value,
    and consumer secret as the second
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    api_keys: dict[str, str] = {}
    KEYS: configparser.SectionProxy = config["KEYS"]  # pylint: disable=C0103
    api_keys["ConsumerKey"] = KEYS["ConsumerKey"]
    api_keys["ConsumerSecret"] = KEYS["ConsumerSecret"]
    api_keys["AccessTokenKey"] = KEYS["AccessTokenKey"]
    api_keys["AccessTokenSecret"] = KEYS["AccessTokenSecret"]

    # FIXME (jam) this naming is godawful
    for key, value in api_keys.items():
        value = expand_tilde(key)
        if Path(value).exists():
            api_keys[key] = read_key(value)

    return api_keys


def write_config(config_file: str):
    """write the config file"""
    if not Path(config_dir).exists():
        Path(config_dir).mkdir(parents=True)
    config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)

    # TODO (jam) check if this comment is valid
    config["KEYS"] = {
        "; Value can be the key itself, or the filepath to a file containing it": "",
        "ConsumerKey": "",
        "ConsumerSecret": "",
        "AccessTokenKey": "",
        "AccessTokenSecret": "",
    }

    try:
        with open(config_file, "w") as configfile:
            config.write(configfile)
    # TODO (jam) handle this differently
    except PermissionError as error:
        SystemExit(error)


def expand_tilde(key: str) -> str:
    """expand the tilde to home path"""
    return str(Path(key).expanduser())


def read_key(location: str) -> str:
    """get key values from locations"""
    with open(location) as file:
        value: str = file.read().strip()
    return value
