from __future__ import print_function

import sqlite3
import json



def create_db():
    conn = sqlite3.connect('twitter_movie_sentiment.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE movies (id INTEGER PRIMARY KEY, name TEXT)''')

    c.execute('''CREATE TABLE keywords (movie_id INTEGER, keyword TEXT, FOREIGN KEY(movie_id) REFERENCES movies(id))''')

    c.execute('''CREATE TABLE tweets (movie_id INTEGER, keyword TEXT, FOREIGN KEY(movie_id) REFERENCES movies(id))''')

    c.execute('''CREATE TABLE ratings (movie_id INTEGER UNIQUE, rating INTEGER, FOREIGN KEY(movie_id) REFERENCES movies(id))''')

files = [
    "data_sets/recent/100_2015_popular_feature_films.txt",
    "data_sets/good/100_best_2014_rt.txt.clean",
    "data_sets/bad/100_worst_all_time_imdb.txt"
]


def clean_data(file_name):
    f = open(file_name, "r")
    lines = f.read().splitlines()
    source = lines[0]
    json_data = lines[1]
    f.close()
    py_json = json.loads(json_data)
    for pair in py_json:
        pair['movie'] = pair['movie'][:-7]
        pair['score'] = str(float(int(pair['score'][:-1]))/float(10))
    new_f = open(file_name + '.clean', "w")
    json.dumps(py_json)
    print(source, file=new_f)
    print(json.dumps(py_json), file=new_f)
    new_f.close


def read_data(file_name):
    f = open(file_name, "r")
    lines = f.read().splitlines()
    f.close()
    source = lines[0]
    json_data = lines[1]
    py_json = json.loads(json_data)
    for pair in py_json:
        print(pair['movie'])

for f in files:
    read_data(f)