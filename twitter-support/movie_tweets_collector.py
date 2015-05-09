#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import string
import tweepy
import io
import datetime
import os


def read_file_lines(file_name):
    f = open(file_name, "r")
    lines = f.read().splitlines()
    f.close()
    return lines


def generate_search_terms(movie):
    movie = str(movie).translate(None, string.punctuation)
    lower_movie = movie.lower()
    parts = movie.split(' ')
    lower_parts = lower_movie.split(' ')
    terms = [
        '#' + '_'.join(lower_parts),
        '@' + '_'.join(lower_parts),
        '_'.join(lower_parts),
        '#' + ''.join(lower_parts),
        '@' + ''.join(lower_parts),
        ''.join(lower_parts),
        movie.lower(),
        movie,
        '#' + '_'.join(parts),
        '@' + '_'.join(parts),
        '#' + ''.join(parts),
        '@' + ''.join(parts),
        ''.join(parts),
        # Quoted
        '"#' + '_'.join(lower_parts) + '"',
        '"@' + '_'.join(lower_parts) + '"',
        '"' + '_'.join(lower_parts) + '"',
        '"#' + ''.join(lower_parts) + '"',
        '"@' + ''.join(lower_parts) + '"',
        '"' + ''.join(lower_parts) + '"',
        '"' + movie.lower() + '"',
        '"' + movie + '"',
        '"#' + '_'.join(parts) + '"',
        '"@' + '_'.join(parts) + '"',
        '"#' + ''.join(parts) + '"',
        '"@' + ''.join(parts) + '"',
        '"' + ''.join(parts) + '"'
    ]
    return terms


def get_tweets(movie):
    auth_data = read_file_lines("auth.txt")
    # get consumer key, consumer secret at https://apps.twitter.com/
    auth = tweepy.OAuthHandler(auth_data[0], auth_data[1])
    # get access token, access token secret at https://apps.twitter.com/
    auth.set_access_token(auth_data[2], auth_data[3])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    all_tweets = []
    terms = generate_search_terms(movie)
    query = " OR ".join(terms)
    print query
    try:
        for status in tweepy.Cursor(api.search, q=query, lang='en', result_type='recent', count=100).items(1000):
            all_tweets.append(status)
    except tweepy.TweepError as e:
        with open('error_log', "a+") as f:
            f.write(str(datetime.datetime.now().time()) + str(e) + "\n")
        return []
    return all_tweets


def main():
    files = [
        "data_sets/recent/",
        "data_sets/good/",
        "data_sets/bad/"
    ]

    for data_dir in files:
        if not os.path.exists(data_dir + 'tweets'):
            os.makedirs(data_dir + 'tweets')
        complete_file = data_dir + 'complete'
        with io.open(complete_file, "a+", encoding="utf-8") as f:
            movies_done = f.read().splitlines()
        with open(data_dir + 'movies.json', "r") as f:
            py_json = json.load(f)
        for pair in py_json['movies']:
            movie = pair['movie']
            if movie not in movies_done:
                tweets = get_tweets(movie)
                json_tweets = []
                if tweets:
                    for tweet in tweets:
                        json_tweets.append({"tweet_text": tweet.text})
                    with open(data_dir + 'tweets/' + '_'.join(movie.split(' ')) + '_tweets.json', 'w+') as f:
                        f.write(json.dumps(json_tweets))
                    with io.open(complete_file, "a+", encoding="utf-8") as f:
                        line = movie + "\n"
                        f.write(line)

if __name__ == '__main__':
    main()