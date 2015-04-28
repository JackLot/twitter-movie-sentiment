from metamind.api import set_api_key, twitter_text_classifier, ClassificationData, ClassificationModel, set_api_key
import os, re

#Set the metamind API key for my account
set_api_key("IpdP8N0nsPmYstaqwqL1CWpPWfxxETCj5BzQWa7ANN6ChZ9PYS")

#Load the classifier we trained on the 3 class Rotten Tomatoes movie reviews
classifier = ClassificationModel(id=25412)

#Define the file paths to our data
tsv_tweets = "datasets/tweets/"
tweets_out = "datasets/tweets_out/"
tweet_types = ["recent"]

#Loop through each folder of good, bad and recent tweets and run
#the classifier on it
for type in tweet_types:

	rel_path = tsv_tweets + type + "/"
	rel_out_path = tweets_out + type + "/"

	#Loop through each movie tweet file
	for movie_tweets_file in os.listdir(rel_path):

		movie_name = movie_tweets_file[:-4]

		print "Predicting... " + rel_path + movie_tweets_file

		#Write the output to a new file
		f = open(rel_out_path + movie_name + ".json", 'w')
		print >>f, classifier.predict(rel_path + movie_tweets_file, input_type="tsv")
		f.close()

		print "  Done!"
		