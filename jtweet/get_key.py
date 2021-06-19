# -*- coding: utf-8 -*-
"""get api key values from strings or keyfiles"""
from __future__ import annotations
import configparser
from pathlib import Path


# TODO (jam) function to write the config
def get_config(config_file: str) -> dict[str, str]:
    """get options from config file
    return api_api_keys, a list with the consumer key as the first value,
    and consumer secret as the second
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    api_keys: dict[str, str] = {}
    api_keys["ConsumerKey"] = config["KEYS"]["ConsumerKey"]
    api_keys["ConsumerSecret"] = config["KEYS"]["ConsumerSecret"]
    api_keys["AccessTokenKey"] = config["KEYS"]["AccessTokenKey"]
    api_keys["AccessTokenSecret"] = config["KEYS"]["AccessTokenSecret"]

    # FIXME (jam) this naming is godawful
    for key, value in api_keys.items():
        value = expand_tilde(key)
        if Path(value).exists():
            api_keys[key] = read_key(value)

    return api_keys


def expand_tilde(key: str) -> str:
    """expand the tilde to home path"""
    return str(Path(key).expanduser())


def read_key(location: str) -> str:
    """get key values from locations"""
    with open(location) as file:
        value: str = file.read().strip()
    return value
