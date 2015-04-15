from metamind.api import set_api_key, twitter_text_classifier, ClassificationData, ClassificationModel, set_api_key

set_api_key("5eqwiKI50ym253djlf84VEgQptIb5odohKFpgS1SSWOdeGDzQ3")

#Using the MetaMind API we can look up things 
#print twitter_text_classifier.query_and_predict("comcast")

# 
training_data = ClassificationData(private=True, data_type="text", name="RT snippets training data")
training_data.add_samples()

classifier = ClassificationModel(private=True, name="RT movie classifier")
classifier.fit(training_data)

print classifier.predict("This company is the worst and is losing money", input_type="text")