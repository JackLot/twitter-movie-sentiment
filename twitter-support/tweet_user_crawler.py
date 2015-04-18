#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json, string, tweepy, codecs, io, datetime

def read_file_lines(file_name):
    f = open(file_name, "r")
    lines = f.read().splitlines()
    f.close()
    return lines

def generate_search_terms(movie):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    movie = movie.translate(remove_punctuation_map)
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
        ''.join(parts)
    ]
    print(terms)
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
    print(query)
    try:
        for status in tweepy.Cursor(api.search, q=query, lang='en', result_type='recent', count=100).items(1000):
            all_tweets.append(status)
    except tweepy.TweepError as e:
        with open('error_log', "a+") as f:
            f.write(str(datetime.datetime.now().time()) + str(e) + "\n")
        return False
    return all_tweets


def main():
    files = {
        "data_sets/recent/100_2015_popular_feature_films.txt": "data_sets/recent/tweets/",
        "data_sets/good/100_best_2014_rt.txt.clean": "data_sets/good/tweets/",
        "data_sets/bad/100_worst_all_time_imdb.txt": "data_sets/bad/tweets/"
    }

    for file_name, data_dir in files.iteritems():
        complete_file = data_dir + 'complete'
        print(complete_file)
        with io.open(complete_file, "r", encoding="utf-8") as f:
            movies_done = f.read().splitlines()
            print(movies_done)
        with open(file_name, "r") as f:
            lines = f.read().splitlines()
        json_data = lines[1]
        py_json = json.loads(json_data)
        for pair in py_json:
            movie = pair['movie']
            if movie not in movies_done:
                tweets = get_tweets(movie)
                json_tweets = []
                if tweets is not False:
                    for tweet in tweets:
                        json_tweets.append({"tweet_text": tweet.text})
                    with open(data_dir + '_'.join(movie.split(' ')) + '_tweets.json', 'w+') as f:
                        f.write(json.dumps(json_tweets))
                    with io.open(complete_file, "a+", encoding="utf-8") as f:
                        line = movie + "\n"
                        f.write(line)

if __name__ == '__main__':
    main()
