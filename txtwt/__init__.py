# -*- coding: utf-8 -*-
"""variables to import"""
from appdirs import user_config_dir
from requests import exceptions

NAME: str = "txtwt"
AUTHOR: str = "sudo-julia"
VERSION: str = "0.1.0"

conf_dir: str = f"{user_config_dir(NAME, AUTHOR)}/config.ini"


def handle_exception(status_code: int):
    """logic tree for handling various http[s] response codes"""
    if status_code == 403:
        raise SystemExit()
    if status_code == 408:
        raise SystemExit(exceptions.Timeout)
    raise SystemExit(exceptions.RequestException)
