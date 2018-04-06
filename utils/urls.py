#!/usr/bin/env python

"""
Print out the URLs in a tweet json stream.
"""
from __future__ import print_function

import json
import fileinput


def extract_tweets(tweet):
    tweets = list()
    tweets.append(tweet)
    if 'quoted_status' in tweet:
        tweets.extend(extract_tweets(tweet['quoted_status']))
    elif 'retweeted_status' in tweet:
        tweets.extend(extract_tweets(tweet['retweeted_status']))
    return tweets


def extract_entity_urls(tweet):
    urls = set()
    entities = tweet.get('extended_tweet', {}).get('entities') or tweet.get('entities', {})
    for url_sect in entities.get('urls', []):
        if 'expanded_url' in url_sect:
            urls.add(url_sect['expanded_url'].encode('utf8'))
    return urls


if __name__ == '__main__':
    for line in fileinput.input():
        for tweet in extract_tweets(json.loads(line)):
            for url in extract_entity_urls(tweet):
                print(url)
