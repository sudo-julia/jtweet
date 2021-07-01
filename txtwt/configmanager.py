# -*- coding: utf-8 -*-
"""
configuration file operations
"""
from __future__ import annotations
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import Dict
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
        template: Dict[str, Dict[str, str]],
        config_file=None,
    ):
        """
        parameters:
            project: str
                the name of the project
            template: Dict[str, Dict[str, str]]
                a dictionary containing the expected configuration template
            config_file: str | Path, optional (default: self.config_file)
                the location of the configuration file
        """
        self.project = project
        self.template = template
        config_dir: str = appdirs.user_config_dir(self.project)
        self.config_file: str | Path = config_file or f"{config_dir}/config.ini"

    def read_config(self, config_file: str | Path = None) -> Dict[str, Dict[str, str]]:
        """
        reads sections from an ini file
        returns a dictionary of dictionaries, {"section": {"key": "value"}}

        parameters:
            config_file: str | Path, optional (default: self.config_file)
                the configuration file to read from
        """
        config_file = config_file or self.config_file
        config_file = Path(config_file)
        parser: ConfigParser = ConfigParser()

        # get values from the config file, create it if it doesn't exist
        try:
            with open(config_file) as file:
                fixed = file.read().format(**self.template)
            parser.read_file(StringIO(fixed))
        except FileNotFoundError:
            print("Config file not found. Creating one now...")
            self.write_config(config_file)
            print("Run script again to use the new config file.")
            SystemExit()
        except PermissionError as error:
            raise error from SystemError()

        configuration: Dict[str, Dict[str, str]] = {
            s: dict(parser.items(s)) for s in parser.sections()
        }

        # grab the section containing keys
        keys: Dict[str, str] = {}
        key_sec: str = ""
        for section in configuration.keys():
            if "key" in section.casefold():
                key_sec = section
                keys = configuration[section].copy()
                break
        if not keys and not key_sec:
            SystemError()

        # read any keyfiles and update configuration dictionary
        for key, value in keys.items():
            # skip over comments
            if key[0] == ";" or not value:
                continue
            value = Path(value).expanduser()
            if value.exists():
                keys[key] = read_key(value)

        configuration[key_sec] = keys
        return configuration

    def write_config(self, config_file: str | Path = None):
        """
        writes a default template to a configuration file

        parameters:
            config_file: str | Path, optional (default: self.config_file)
                the configuration file to read from
        """
        config_file = config_file or self.config_file
        config_file = Path(config_file)
        parser: ConfigParser = ConfigParser(allow_no_value=True)

        # populate the config file with the template
        for section in self.template.keys():
            parser[section] = self.template[section]

        try:
            if not config_file.parent.exists():
                config_file.parent.mkdir(parents=True)
            with config_file.open("w") as configfile:
                parser.write(configfile)
        except PermissionError as error:
            raise error from SystemError()

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
