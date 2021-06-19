# -*- coding: utf-8 -*-
"""send tweets from textfiles"""
import sys
import logging
from TwitterAPI import TwitterAPI
from appdirs import user_log_dir
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from jtweet import handle_exception, NAME


def post_tweet(status: str) -> bool:
    """check a status for character length, and post the tweet"""
    # TODO (jam) make this read what file was trying to be read from. exit w/o sorting
    if len(status) > 280:
        raise NotImplementedError
    api: TwitterAPI = TwitterAPI("", "", "", "")
    tweet = api.request("statuses/update", {"status": status})
    if tweet.status_code != 200:
        handle_exception(tweet.status_code)
    return True


def main():
    """:"""
    # TODO (jam) inform user of log location, add section in config
    logging.basicConfig(
        filename=user_log_dir(NAME),
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )
    # TODO (jam) set this path to whatever dir the user sets in config
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
