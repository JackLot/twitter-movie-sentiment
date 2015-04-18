from __future__ import print_function

import sqlite3,json, string, tweepy, stdout


class MyListener(tweepy.StreamListener):

    def __init__(self, movie, data_dir):
        self.temp_data = []
        self.movie = movie
        self.data_dir = data_dir
        super(MyListener, self).__init__(self)

    def on_data(self, data):
        self.temp_data.append(data.strip() + "\n")
        stdout.write("\rFor movie %s collected %d tweets" % (self.movie, len(self.temp_data)))
        stdout.flush()
        if len(self.temp_data) == 1000:
            content = ''.join(self.temp_data)
            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
            file_name = '_'.join(self.movie.translate(remove_punctuation_map).split(' ')) + ".json"
            f = open(self.data_dir + file_name, 'w')
            f.write(content)
            f.close()
            return False


def read_file_lines(file_name):
    f = open(file_name, "r")
    lines = f.read().splitlines()
    f.close()
    return lines


def create_db():
    conn = sqlite3.connect('twitter_movie_sentiment.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE movies (id INTEGER PRIMARY KEY, name TEXT)''')

    c.execute('''CREATE TABLE keywords (movie_id INTEGER, keyword TEXT, FOREIGN KEY(movie_id) REFERENCES movies(id))''')

    c.execute('''CREATE TABLE tweets (movie_id INTEGER, keyword TEXT, FOREIGN KEY(movie_id) REFERENCES movies(id))''')

    c.execute('''CREATE TABLE ratings (movie_id INTEGER UNIQUE, rating INTEGER, FOREIGN KEY(movie_id) REFERENCES movies(id))''')


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
    new_f.close()


def generate_stream_track_terms(movie):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    movie = movie.translate(remove_punctuation_map)
    lower_movie = movie.lower()
    parts = movie.split(' ')
    lower_parts = lower_movie.split(' ')
    terms = [
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


def main():
    auth_data = read_file_lines("auth.txt")
    # get consumer key, consumer secret at https://apps.twitter.com/
    auth = tweepy.OAuthHandler(auth_data[0], auth_data[1])
    # get access token, access token secret at https://apps.twitter.com/
    auth.set_access_token(auth_data[2], auth_data[3])
    api = tweepy.API(auth)

    files = {
        "data_sets/recent/100_2015_popular_feature_films.txt": "data_sets/recent/tweets/",
        "data_sets/good/100_best_2014_rt.txt.clean": "data_sets/good/tweets/",
        "data_sets/bad/100_worst_all_time_imdb.txt": "data_sets/bad/tweets/"
    }

    i = 0
    for file_name, data_dir in files.iteritems():
        f = open(file_name, "r")
        lines = f.read().splitlines()
        f.close()
        json_data = lines[1]
        py_json = json.loads(json_data)
        for pair in py_json:
            stream_listener = MyListener(pair['movie'], data_dir)
            stream = tweepy.Stream(auth=api.auth, listener=stream_listener, secure=True)
            stream.filter(track=generate_stream_track_terms(pair['movie']))


if __name__ == '__main__':
    main()