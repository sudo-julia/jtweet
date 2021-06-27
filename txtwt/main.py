# -*- coding: utf-8 -*-
"""send tweets from textfiles"""
from __future__ import annotations
from argparse import ArgumentParser, _ArgumentGroup, Namespace
from TwitterAPI import TwitterAPI
from txtwt import handle_exception, conf_dir, VERSION
from txtwt.configmanager import ConfigManager


def post_tweet(status: str, keys: dict[str, str]) -> bool:
    """check a status for character length, and post the tweet"""
    # TODO (jam) make this read what file was trying to be read from. exit w/o sorting
    if len(status) > 280:
        print("Tweet too long.")
        raise NotImplementedError
    api: TwitterAPI = TwitterAPI(
        keys["consumer_key"],
        keys["consumer_secret"],
        keys["access_token_key"],
        keys["access_token_secret"],
    )
    tweet = api.request("statuses/update", {"status": status})
    if tweet.status_code != 200:
        handle_exception(tweet.status_code)
    return True


def main():
    """start the watchdog"""
    parser: ArgumentParser = ArgumentParser()
    post_args: _ArgumentGroup = parser.add_mutually_exclusive_group()
    main_args: _ArgumentGroup = parser.add_argument_group()
    post_args.add_argument("-b", "--bio", help="update your bio")
    post_args.add_argument("-t", "--tweet", help="post a tweet")
    main_args.add_argument(
        "-c",
        "--config",
        default=conf_dir,
        help="Use this config file",
    )
    main_args.add_argument("--version", action="version", version=f"txtwt v{VERSION}")

    args: Namespace = parser.parse_args()
    myconf = ConfigManager("txtwt", config_file=args.config)
    myvars = myconf.read_config()
    del myvars


if __name__ == "__main__":
    main()
