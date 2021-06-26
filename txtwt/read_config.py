# -*- coding: utf-8 -*-
"""get api key values from strings or keyfiles"""
from __future__ import annotations
from configparser import ConfigParser, SectionProxy
from pathlib import Path
import appdirs
from txtwt import NAME, AUTHOR


# TODO (jam) document the entire class
class Config:
    """
    configuration file manager

    attributes:
        config_file: str
            a path to the configuration file.
            defaults to {config_dir}/config.ini

    methods:
        read_config(config_file: str)
            reads a configuration file and returns the found values
        write_config(config_file: str)
            writes a configuration file
    """

    def __init__(
        self,
        config_file: str | Path = None,
        template=None,
    ):
        """
        parameters:
            config_file: str | Path = None
                the location of the configuration file
        """
        config_dir: str = f"{appdirs.user_config_dir(NAME, AUTHOR)}"
        self.config_file: str | Path = config_file or f"{config_dir}/config.ini"
        # TODO (jam) create config sections with a loaded template, as opposed to static
        self.template = template or {}

    def read_config(self, config_file: str | Path = None) -> dict[str, dict[str, str]]:
        """get options from config file
        return api_api_keys, a list with the consumer key as the first value,
        and consumer secret as the second
        """
        config_file = config_file or self.config_file
        config_file = Path(config_file)
        config = ConfigParser()
        config.read(config_file)

        try:
            config.read(config_file)
        except FileNotFoundError:
            print("Config file not found. Creating one now...")
            self.write_config(config_file)
        except PermissionError as error:
            raise SystemExit from error

        config_info: dict[str, dict[str, str]] = {}
        config_info["keys"] = {}
        config_info["locations"] = {}

        keys: SectionProxy = config["KEYS"]
        config_info["keys"]["consumer_key"] = keys["consumer_key"]
        config_info["keys"]["consumer_secret"] = keys["consumer_secret"]
        config_info["keys"]["access_token_key"] = keys["AccessTokenKey"]
        config_info["keys"]["access_token_secret"] = keys["access_token_secret"]

        locations: SectionProxy = config["LOCATIONS"]
        config_info["locations"]["tweet_dir"] = locations["tweet_dir"]
        config_info["locations"]["log_location"] = locations["log_location"]

        for key, value in config_info["keys"].items():
            value = expand_tilde(key)  # value gets returned as a Path object
            if value.exists():
                config_info["keys"][key] = read_key(value)

        return config_info

    def write_config(self, config_file: str | Path = None):
        """write the config file"""
        config_file = config_file or self.config_file
        config_file = Path(config_file)

        config: ConfigParser = ConfigParser(allow_no_value=True)

        config["KEYS"] = {  # type: ignore
            "; Value can be the key itself or a filepath to a file containing it": None,
            "consumer_key": "",
            "consumer_secret": "",
            "access_token_key": "",
            "access_token_secret": "",
        }

        config["LOCATIONS"] = {  # type: ignore
            f"; tweet_dir is the location that {NAME} will watch for new tweets.": None,
            "tweet_dir": appdirs.user_data_dir(NAME),
            "; Location of the logfile": None,
            "log_location": appdirs.user_log_dir(NAME),
        }

        try:
            if not config_file.parent.exists():
                config_file.parent.mkdir(parents=True)
            with config_file.open("w") as configfile:
                config.write(configfile)
        except PermissionError as error:
            raise SystemExit from error

        print(f"Configuration file created at {config_file}")


def expand_tilde(key: str) -> Path:
    """expand the tilde to home path"""
    return Path(key).expanduser()


def read_key(location: Path) -> str:
    """get key values from locations"""
    with location.open() as file:
        value: str = file.read().strip()
    return value
