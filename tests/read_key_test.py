# -*- coding: utf-8 -*-
"""test read_key"""
from pathlib import Path
from tempfile import NamedTemporaryFile
from txtwt.configmanager import read_key


def test_read_key():
    """test read_key"""
    with NamedTemporaryFile("w+", suffix=".txt") as tmpf:
        tmpf.write("trailing spaces    ")
        tmpf.seek(0)
        assert read_key(Path(tmpf.name)) == "trailing spaces"

    with NamedTemporaryFile("w+", suffix=".txt") as tmpf:
        tmpf.write("    wrapped in spaces  ")
        tmpf.seek(0)
        assert read_key(Path(tmpf.name)) == "wrapped in spaces"
