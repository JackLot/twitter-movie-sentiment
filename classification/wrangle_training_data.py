import csv
import re

#Credit: This file is slightly modified from the original source found here:
#http://mlwave.com/movie-review-sentiment-analysis-with-vowpal-wabbit/

#The original TSV files headers: PhraseId  SentenceId  Phrase  Sentiment
#Sentiment is a number from 0 - 4 (negative, somewhat negative, neutral, somewhat positive, positive)
original_train = "datasets/rt/train.tsv"
original_test = "datasets/rt/test.tsv"

#The name of the MetaMind output files we want to create
mm_train = "rt.train.tsv"
mm_test = "rt.test.tsv"

mm_train_3 = "rt.train-3.tsv"
mm_test_3 = "rt.test-3.tsv"

#Remove irrelevant characters from a string
def clean(s):
  return " ".join(re.findall(r'\w+', s,flags = re.UNICODE | re.LOCALE)).lower()

#Reduce a 5 value sentiment to 3 values
def reduceSentiment(sentiment):
  temp = int(sentiment) + 1

  #Somewhat negative becomes negative
  if temp == 2:
    temp = temp - 1

  #Somewhat positive becomes positive
  if temp == 4:
    temp = temp + 1

  return str(temp)

#Creates MetaMind formatted file from tsv file
def to_vw(input_file, output_file, test = False, numFeatures = 5):

  print "\nReading:",input_file,"\nWriting:",output_file

  with open(input_file) as infile, open(output_file, "wb") as outfile:

    #Create reader to read in tab separated values file
    reader = csv.DictReader(infile, delimiter="\t")

    #Loop through every line of the input file
    for row in reader:

      phrase = clean(row['Phrase'])

      #If we are creating the test dataset then ignore the label
      if test:
        outline = phrase + "\n"
      else:
        if numFeatures == 3:
          outline = reduceSentiment(row['Sentiment']) + "\t" + phrase + "\n"
        else:
          outline = str(int(row['Sentiment'])+1) + "\t" + phrase + "\n"

      #outfile.write(label + " '"+row['PhraseId'] + " |f " + phrase + " |a " + "word_count:"+str(phrase.count(" ")+1) + "\n" )
      outfile.write(outline)

# Create our train and test files 
#(create two test/train sets: one with 5 features (with somewhats positive/negative) and one with only 3 (pos, neg, neutral))
to_vw(original_train, mm_train)
to_vw(original_test, mm_test, test=True)

to_vw(original_train, mm_train_3, numFeatures=3)
to_vw(original_test, mm_test_3, test=True, numFeatures=3)