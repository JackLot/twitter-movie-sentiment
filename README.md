# Twitter Movie Sentiment Analysis
Given a set of tweets about a movie determine if the Twitter community has a positive or negative overall opinion of that movie

## Training/Test data
Since this problem hasn't been studied much before we will train our models with datasets that are closely related
to our problem: movie reviews on movie review websites (i.e. Rotten Tomatoes).

We used a dataset from Kaggle.com -- [Sentiment Analysis on Movie Reviews dataset] (http://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/data) -- 
which provided us with a file containing snippets of movie reviews 
along with the sentiment associated with each part of the sentence (Sentiment => 0: negative, 1: somewhat negative, 2: neutral, 3: somewhat positive, 4: positive)
```
PhraseId	SentenceId	Phrase	Sentiment
104	3	have a hard time sitting through this one	0
105	3	have	2
106	3	a hard time sitting through this one	1
107	3	a hard time	1
108	3	hard time	1
...
```

## Data Wrangling

Using Python scripts we had to reformat the data from Kaggle into files readable by Vowpal Wabbit and MetaMind.

#### MetaMind formatting

By running [classification/wrangle_mm.py](classification/wrangle_mm.py) 
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

We'll start off by building a text classifier with the MetaMind API trained on a dataset of Rotten Tomatoes
movie reviews.

MetaMind is a new API service that allows users to get up and running quickly with 
text classification and ML. MetaMind has its own Twitter Sentiment classifier pre-built, 
but for this project we created our own classifer by feeding the MetaMind classification 
model builder formatted training data from the Kaggle Rotten Tomatoes dataset.

From [classification/build_classifier_mm.py](classification/build_classifier_mm.py)
```python
#Create the classification training data to feed into the model
training_data = ClassificationData(private=True, data_type="text", name="RT snippets 3 feature training data")
training_data.add_samples("rt.train-3.tsv", input_type="tsv")

#Train the classifier
classifier = ClassificationModel(private=True, name="RT movie 3-value classifier")
classifier.fit(training_data)
```
