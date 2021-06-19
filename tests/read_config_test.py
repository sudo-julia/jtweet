# -*- coding: utf-8 -*-
"""test read_config"""
from __future__ import annotations
from configparser import ConfigParser
from pathlib import Path
from tempfile import NamedTemporaryFile
from jtweet.read_config import read_config


def test_read_config():
    """test read_config"""
    accesstokenkey = NamedTemporaryFile("w+", prefix="tmpacctoken")
    accesstokenkey.write("    accesstokenkey")
    accesstokenkey.seek(0)
    with NamedTemporaryFile("w", suffix=".ini") as tmpconf:
        config: ConfigParser = ConfigParser()
        config["KEYS"] = {
            "ConsumerKey": "consumerkey",
            "ConsumerSecret": "CONSUMERSECRET",
            "AccessTokenKey": accesstokenkey.name,
            "AccessTokenSecret": "AccessTokenSecret",
        }

        config["LOCATIONS"] = {
            "TweetDir": str(Path().home()),
            "LogLocation": "/fake/log/dir",
        }

        # FIXME (jam) something here isn't working
        config.write(tmpconf)
        conf: dict[str, dict[str, str]] = read_config(tmpconf.name)

    assert conf["keys"]["ConsumerKey"] == "consumerkey"
    assert conf["keys"]["ConsumerSecret"] == "CONSUMERSECRET"
    assert conf["keys"]["AccessTokenKey"] == "accesstokenkey"
    assert conf["keys"]["AccessTokenSecret"] == "AccessTokenSecret"
    assert conf["locations"]["TweetDir"] == str(Path().home())
    assert conf["locations"]["LogLocation"] == "/fake/log/dir"
    accesstokenkey.close()
