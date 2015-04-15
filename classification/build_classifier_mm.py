from metamind.api import set_api_key, twitter_text_classifier, ClassificationData, ClassificationModel, set_api_key

set_api_key("5eqwiKI50ym253djlf84VEgQptIb5odohKFpgS1SSWOdeGDzQ3")

#Using the MetaMind API we can look up things 
#print twitter_text_classifier.query_and_predict("comcast")

#Create the classification training data to feed into the model
training_data = ClassificationData(private=True, data_type="text", name="RT snippets 3 feature training data")
training_data.add_samples("rt.train-3.tsv", input_type="tsv")

#Train the classifier
classifier = ClassificationModel(private=True, name="RT movie 3-value classifier")
classifier.fit(training_data)

#print classifier.predict("Furious7 was the worst movie I've ever seen. Period.", input_type="text")