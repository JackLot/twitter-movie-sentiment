from metamind.api import set_api_key, twitter_text_classifier, ClassificationData, ClassificationModel, set_api_key

#Set the metamind API key for my account
set_api_key("IpdP8N0nsPmYstaqwqL1CWpPWfxxETCj5BzQWa7ANN6ChZ9PYS")

#Load the classifier we trained on the 3 class Rotten Tomatoes movie reviews
classifier = ClassificationModel(id=25412)

tsv_tweets_out = "datasets/tweets/"
tweet_types = ["good", "bad", "recent"]

print classifier.predict("datasets/tweets/good/The_Imitation_Game.tsv", input_type="tsv")