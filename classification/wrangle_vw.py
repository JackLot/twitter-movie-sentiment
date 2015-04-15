import csv
import re

#Credit: This file is slightly modified from the original source found here:
#http://mlwave.com/movie-review-sentiment-analysis-with-vowpal-wabbit/

#The original TSV files headers: PhraseId  SentenceId  Phrase  Sentiment
#Sentiment is a number from 0 - 4 (negative, somewhat negative, neutral, somewhat positive, positive)
original_train = "datasets/rt/train.tsv"
original_test = "datasets/rt/test.tsv"

#The name of the output files we want to create
vw_train = "rt.train.vw"
vw_test = "rt.test.vw"

#Remove irrelevant characters from a string
def clean(s):
  return " ".join(re.findall(r'\w+', s,flags = re.UNICODE | re.LOCALE)).lower()

#Creates Vowpal Wabbit-formatted file from tsv file
#Will output like: 3 '11 |f demonstrating the adage |a word_count:3
def to_vw(input_file, output_file, test = False):

  print "\nReading:",input_file,"\nWriting:",output_file

  with open(input_file) as infile, open(output_file, "wb") as outfile:

    #Create reader to read in tab separated values file
    reader = csv.DictReader(infile, delimiter="\t")

    #Loop through every line of the input file
    for row in reader:
      #If we are creating the test dataset then the label doesn't matter (won't be used)
      if test:
        label = "1"
      else:
        label = str(int(row['Sentiment'])+1)

      phrase = clean(row['Phrase'])
      outfile.write(label + " '"+row['PhraseId'] + " |f " + phrase + " |a " + "word_count:"+str(phrase.count(" ")+1) + "\n" )

# Create our train and test files
to_vw(original_train, vw_train)
to_vw(original_test, vw_test, test=True)