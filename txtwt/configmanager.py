# -*- coding: utf-8 -*-
"""
configuration file operations
"""
from __future__ import annotations
from configparser import ConfigParser, SectionProxy
from pathlib import Path
import appdirs


class ConfigManager:
    """
    configuration file manager

    attributes:
        project: str
            the name of the project - used to create directories
        config_file: str
            a path to the configuration file.
            defaults to {config_dir}/config.ini

    methods:
        read_config(config_file: str | Path = None)
            reads a configuration file and returns the found values
        write_config(config_file: str | Path = None)
            writes a configuration file
    """

    def __init__(
        self,
        project: str,
        config_file: str | Path = None,
        template=None,
    ):
        """
        parameters:
            project: str
                the name of the project
            config_file: str | Path, optional (default: self.config_file)
                the location of the configuration file
        """
        self.project = project
        config_dir: str = f"{appdirs.user_config_dir(self.project)}"
        self.config_file: str | Path = config_file or f"{config_dir}/config.ini"
        # TODO (jam) create config sections with a loaded template, as opposed to static
        self.template = template or {}

    def read_config(self, config_file: str | Path = None) -> dict[str, dict[str, str]]:
        """
        reads sections from an ini file
        returns a dictionary of dictionaries, {"section": {"key": "value"}}

        parameters:
            config_file: str | Path, optional (default: self.config_file)
                the configuration file to read from
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
        config_info["locations"]["log_location"] = locations["log_location"]

        for key, value in config_info["keys"].items():
            value = Path(value).expanduser()
            if value.exists():
                config_info["keys"][key] = read_key(value)

        return config_info

    def write_config(self, config_file: str | Path = None):
        """
        writes a default template to a configuration file

        parameters:
            config_file: str | Path, optional (default: self.config_file)
                the configuration file to read from
        """
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
            "; Location of the logfile": None,
            "log_location": appdirs.user_log_dir(self.project),
        }

        try:
            if not config_file.parent.exists():
                config_file.parent.mkdir(parents=True)
            with config_file.open("w") as configfile:
                config.write(configfile)
        except PermissionError as error:
            raise SystemExit from error

        print(f"Configuration file created at {config_file}")


def read_key(location: Path) -> str:
    """
    reads a key from a text file containing one line

    parameters:
        location: Path
            the location of the file to read from
    """
    with location.open() as file:
        return file.read().strip()
