## File overview

* **[wrangle_training_data.py](wrangle_training_data.py)**: Takes raw train/test data from Kaggle (found here: [datasets/rt/](datasets/rt/)) and converts it to a MetaMind useable TSV formats. It creates a 5-class train/test set ([rt.test.tsv](rt.test.tsv), [rt.train.tsv](rt.train.tsv)) and a 3-class train/test set ([rt.test-3.tsv](rt.test-3.tsv), [rt.train-3.tsv](rt.train-3.tsv))

* **[wrangle_tweets.py](wrangle_tweets.py)**: Takes the raw tweets from ([../twitter-support/datasets/](../twitter-support/datasets/)) and formats them as unlabeled TSV files for use by MetaMind. The newely formatted tweets (ready for classification) are written to [datasets/tweets/](datasets/tweets/).

* **[build_classifier_mm.py](build_classifier_mm.py)**: Takes a training and test test dataset (in our case [rt.test-3.tsv](rt.test-3.tsv), [rt.train-3.tsv](rt.train-3.tsv)) and uses the MetaMind API to train a classifier on the data. The classifier is stored in the cloud by an id number which is referenced by our classification program ([classify_mm.py](classify_mm.py))

* **[classify_mm.py](classify_mm.py)**: Reads unclassified tweets from [datasets/tweets/](datasets/tweets/) and predicts their labels (as either positive, negative or neutral). The labeled data is output as JSON to [datasets/tweets-out/](datasets/tweets-out/) for use by our web application.


## Training/Test data
Since this problem hasn't been studied much before we will train our models with datasets that are closely related
to our problem: movie reviews on movie review websites (i.e. Rotten Tomatoes).

We used a dataset from Kaggle.com -- [Sentiment Analysis on Movie Reviews dataset] (http://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/data) -- 
which provided us with a file containing snippets of movie reviews 
along with the sentiment associated with each part of the sentence (Sentiment => 0: negative, 1: somewhat negative, 2: neutral, 3: somewhat positive, 4: positive)

Training data [datasets/rt/train.tsv](datasets/rt/train.tsv)
```
PhraseId	SentenceId	Phrase	Sentiment
104	3	have a hard time sitting through this one	0
105	3	have	2
106	3	a hard time sitting through this one	1
107	3	a hard time	1
108	3	hard time	1
...
```
note: All training/testing data can be found at [datasets/rt/](datasets/rt/)

## Data Wrangling

Using Python scripts we had to reformat the data from Kaggle into files readable by MetaMind.

#### MetaMind formatting

By running [classification/wrangle_training_data.py](classification/wrangle_training_data.py) 
we output train/test files (rt.train.tsv, rt.test.tsv, rt.train-3.tsv and rt.test-3.tsv) for use with MetaMind's classifier
building tools. 
```
3	occasionally
3	amuses but none of which amounts to much of a story
5	amuses
1	but none of which amounts to much of a story
3	but
1	none of which amounts to much of a story
3	none
```
(Note: rt.train-3.tsv and rt.test-3.tsv files simply transform the *somewhat negative* and *somewhat positive* sentiments into just
*negative* and *positive* respectively so there are just 3 classes for the classifier to worry about)



## Classification with MetaMind

MetaMind is a new API service that allows users to get up and running quickly with 
text classification and ML. MetaMind has its own Twitter Sentiment classifier pre-built, 
but for this project we created our own classifer by feeding the MetaMind classification 
model builder formatted training data from the Kaggle Rotten Tomatoes dataset.


### Building the classification model

We'll start off by building a text classifier with the MetaMind API trained on a dataset of Rotten Tomatoes
movie reviews.

From [classification/build_classifier_mm.py](classification/build_classifier_mm.py)
```python
#Create the classification training data to feed into the model
training_data = ClassificationData(private=True, data_type="text", name="RT snippets 3 feature training data")
training_data.add_samples("rt.train-3.tsv", input_type="tsv")

#Train the classifier
classifier = ClassificationModel(private=True, name="RT movie 3-value classifier")
classifier.fit(training_data)
```

### Running the classifier

When we ran the classifier against tweets that we have pulled using the Twitter API, MetaMind gives us output as a JSON list of JSON objects containing our input tweet as well as a label it predicted for that Tweet.

```
[
  {u'user_value': u"Furious7 was the worst movie I've ever seen. Period.", u'probability': 0.819143650919281, u'label': u'1'}, 
  {u'user_value': u'I loved Skyfall. Brilliant!', u'probability': 0.9619668949957287, u'label': u'5'}
]
```
<small><i>note: Output is given for the 3-class model where 1:negative, 3:neutral and 5:positive)</i></small>


## Analyzing our results

Now all that is left is to take the results of feeding our MetaMind and Vowpal Wabbit classifiers tweets, and determine if the number of positive tweets outweights the number of negative tweets (I think we can ignore neutral tweets). We can then compare our overall ranking of positive/negative for the given movie to the RottenTomatoes and IMDb user reviews to see how accuratly we can classify movies just based on tweets.
