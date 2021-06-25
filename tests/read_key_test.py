# -*- coding: utf-8 -*-
"""test read_key"""
from tempfile import NamedTemporaryFile
from txtwt.read_config import read_key


def test_read_key():
    """test read_key"""
    with NamedTemporaryFile("w+", suffix=".txt") as tmpf:
        tmpf.write("trailing spaces    ")
        tmpf.seek(0)
        assert read_key(tmpf.name) == "trailing spaces"

    with NamedTemporaryFile("w+", suffix=".txt") as tmpf:
        tmpf.write("    wrapped in spaces  ")
        tmpf.seek(0)
        assert read_key(tmpf.name) == "wrapped in spaces"
