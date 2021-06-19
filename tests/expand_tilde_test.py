# -*- coding: utf-8 -*-
"""test expand_tilde"""
from pathlib import Path
from jtweet.read_config import expand_tilde


def test_expand_tilde():
    """test expand_tilde"""
    assert expand_tilde("~") == str(Path.home())
