import csv
import json
import re

json_raw_tweets = "../twitter-support/data_sets/"
tsv_tweets_out = "datasets/tweets/"
tweet_types = ["good", "bad", "recent"]


#Remove irrelevant characters from a string
def clean(s):
  return " ".join(re.findall(r'\w+', s, flags = re.UNICODE | re.LOCALE)).lower()


#Creates MetaMind formatted file from tsv file
def to_mm_tsv(input_file, output_file):

  print "\nReading json from:", input_file,"\nWriting to:", output_file

  f = open(input_file)
  tweets = json.load(f)

  with open(output_file, "wb") as outfile:

    #Loop through every line of the input file
    for tweet in tweets:

      tweet_clean = "-1" + "\t" + clean(tweet["tweet_text"])
      #tweet["tweet_text"].encode('utf-8')
     
      #break
      
      outfile.write(tweet_clean + "\n")


to_mm_tsv(json_raw_tweets+"good/tweets/The_Imitation_Game_tweets.json", tsv_tweets_out+"good/The_Imitation_Game.tsv")