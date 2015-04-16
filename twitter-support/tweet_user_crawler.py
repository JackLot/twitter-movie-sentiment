import tweepy
from sys import stdout


def read_file_lines(file_name):
    f = open(file_name, "r")
    lines = f.read().splitlines()
    f.close()
    return lines


class MyListener(tweepy.StreamListener):

    def __init__(self):
        self.temp_data = []
        self.total_tweets = 0
        super(MyListener, self).__init__(self)

    def on_data(self, data):
        self.temp_data.append(data.strip() + "\n")
        stdout.write("\r%d-%d" % (self.total_tweets, len(self.temp_data)))
        stdout.flush()
        if len(self.temp_data) == 1000:
            file_index = self.total_tweets / 1000
            self.total_tweets += 1000
            f = open("incoming-" + str(file_index), 'a')
            content = ''.join(self.temp_data)
            f.write(content)
            f.close()
            self.temp_data = []

    def on_error(self, status_code):
        print 'Error: ', str(status_code)
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


def main():
    while True:
        key_words = read_file_lines("keywords.txt")
        # Format of auth_data file is:
        # consumer key
        # consumer secret
        # access token
        # access token secret
        auth_data = read_file_lines("auth.txt")
        # get consumer key, consumer secret at https://apps.twitter.com/
        auth = tweepy.OAuthHandler(auth_data[0], auth_data[1])
        # get access token, access token secret at https://apps.twitter.com/
        auth.set_access_token(auth_data[2], auth_data[3])
        api = tweepy.API(auth)
        stream_listener = MyListener()
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener, secure=True)
        stream.filter(track=key_words)


if __name__ == '__main__':
    main()