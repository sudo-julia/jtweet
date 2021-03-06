# -*- coding: utf-8 -*-
"""send tweets from textfiles"""
import sys
import logging
from TwitterAPI import TwitterAPI
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


def post_tweet(status: str) -> bool:
    """check a status for character length, and post the tweet"""
    # TODO (jam) integrate keys (use censearch's config reader)
    api: TwitterAPI = TwitterAPI("", "", "", "")
    tweet = api.request("statuses/update", {"status": status})
    if tweet.status_code != 200:
        raise NotImplementedError
    return True


def main():
    """:"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
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
