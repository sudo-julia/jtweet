# -*- coding: utf-8 -*-
"""parse censearch's config file and return API key values"""
from __future__ import annotations
import configparser
import os


def get_config(config_file: str) -> list[str]:
    """get options from config file
    return api_keys, a list with the consumer key as the first value,
    and consumer secret as the second
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    api_keys: list[str] = []
    api_keys.append(config["KEYS"]["ConsumerKey"])
    api_keys.append(config["KEYS"]["ConsumerSecret"])

    for key in api_keys:
        key_num: int = api_keys.index(key)
        key = expand_tilde(key)
        if os.path.exists(key):
            api_keys[key_num] = read_key(key)

    return api_keys


def expand_tilde(key: str) -> str:
    """expand the tilde to home path"""
    if key[0] == "~":
        key = os.path.expanduser(key)
    return key


def read_key(location: str) -> str:
    """get key values from locations"""
    with open(location) as file:
        value: str = file.read().strip()
    return value
