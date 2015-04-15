#!/bin/bash
 
# Requires vw (https://github.com/JohnLangford/vowpal_wabbit/wiki/),
# the IMDB dataset (http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz),
# and the perf utility from http://osmot.cs.cornell.edu/kddcup/software.html.
 
# Create VW input files for the training data
cat datasets/imdb/train/labeledBow.feat | \
  sed -n 's/^\([7-9]\|10\)\s/&/p' | \
  sed -e "s/^\([7-9]\|10\)\s//" | \
  awk '{ print "1 '"'"'pos_" (NR-1) " |features " $0}' > train.vw
cat datasets/imdb/train/labeledBow.feat | \
  sed -n 's/^[1-4]\s/&/p' | \
  sed -e "s/^[1-4]\s//" | \
  awk '{ print "0 '"'"'neg_" (NR-1) " |features " $0}' >> train.vw

# Create VW input files for the testing data
cat datasets/imdb/test/labeledBow.feat | \
  sed -n 's/^\([7-9]\|10\)\s/&/p' | \
  sed -e "s/^\([7-9]\|10\)\s//" | \
  awk '{ print "1 '"'"'pos_" (NR-1) " |features " $0}' > test.vw
cat datasets/imdb/test/labeledBow.feat | \
  sed -n 's/^[1-4]\s/&/p' | \
  sed -e "s/^[1-4]\s//" | \
  awk '{ print "0 '"'"'neg_" (NR-1) " |features " $0}' >> test.vw

# Use ruby to pull in the actual review text from their individual files by joining on their id
ruby -e 'File.open("audit.vw","w") do |f| f.puts "|features #{(0..89525).to_a.collect {|x| "#{x}:1"}.join(" ")}" end'


rm .cache

shuf train.vw | vw --adaptive --power_t 0.2 -c -f model.dat --passes 200 --l1 5e-8 --l2 5e-8 --sort_features
cat test.vw | cut -d ' ' -f 1 > labels
cat test.vw | vw -t -i model.dat -p pred_out.tmp --quiet
cat audit.vw | vw -t -i model.dat -a --quiet  > audit.log
 
cat pred_out.tmp | cut -d ' ' -f 1 > pred_out
rm pred_out.tmp
 
#perf -files labels pred_out -easy