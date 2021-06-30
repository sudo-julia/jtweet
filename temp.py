# -*- coding: utf-8 -*-
""":"""
from configparser import ConfigParser
from io import StringIO


keys = {
    "API Keys": {
        "consumer_key": "",
        "consumer_secret": "",
        "access_key": "",
        "access_secret": "",
    },
    "Locations": {"log_location": ""},
}

with open("config.ini") as conffile:
    fixed = conffile.read().format(**keys)

parser = ConfigParser()
parser.read_file(StringIO(fixed))
