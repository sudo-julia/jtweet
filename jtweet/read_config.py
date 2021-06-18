# -*- coding: utf-8 -*-
"""read the config.ini file.
if directories are set, override the defaults found by get_xdg
"""
# pylint: disable=import-error
from __future__ import annotations
import configparser
import sys
from pathlib import Path
from appdirs import user_config_dir
from get_xdg import get_dirs  # type: ignore
from jtweet import NAME, AUTHOR, VERSION


config_dir: str | None = user_config_dir(NAME, AUTHOR, VERSION)
# config_dir: str | None = os.environ.get("XDG_CONFIG_HOME")
if not config_dir:
    print("Cannot find config location.")
    sys.exit(1)
config_dir = f"{config_dir}/jtweet"


# TODO (jam) revamp here
def write_config(config_file: str):
    """write the config file"""
    if not Path(config_dir).exists():  # type: ignore
        Path(config_dir).mkdir(parents=True)  # type: ignore
    config = configparser.ConfigParser(allow_no_value=True)
    # pylint: disable=unbalanced-tuple-unpacking
    downloads, documents, music, pictures, videos = get_dirs()
    config["DIRECTORIES"] = {
        "; set the directories to sort downloaded files to": None,
        "; values set here override XDG Dirs": None,
        "Downloads": downloads,
        "Documents": documents,
        "Music": music,
        "Pictures": pictures,
        "Videos": videos,
    }
    with open(config_file, "w") as configfile:
        config.write(configfile)


# TODO (jam) make this relevant again
def read_config() -> list[str]:
    """get options from config.ini"""
    config_file = f"{config_dir}/config.ini"
    config: configparser.ConfigParser = configparser.ConfigParser()
    if not Path(config_file).exists():
        write_config(config_file)
    config.read(config_file)
    dirs: list[str] = []
    for dir_ in dict(config["DIRECTORIES"]).values():
        dirs.append(expand_tilde(dir_))
    return dirs


def expand_tilde(path: str) -> str:
    """expand the tilde to home path"""
    return str(Path(path).expanduser())
