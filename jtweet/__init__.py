# -*- coding: utf-8 -*-
"""variables to import"""
from requests import exceptions

NAME: str = "jtweet"
AUTHOR: str = "sudo-julia"
VERSION: str = "0.1.0"


def handle_exception(status_code: int):
    """logic tree for handling various http[s] response codes"""
    if status_code == 408:
        raise SystemExit(exceptions.Timeout)
    raise SystemExit(exceptions.RequestException)
