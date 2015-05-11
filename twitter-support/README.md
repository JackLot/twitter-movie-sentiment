
#Twitter Support Tool

This tool requires the tweepy module: https://github.com/tweepy/tweepy.

For the purpose of collecting data we wrote movie_tweets_collector.py.
A main method is defined that will be run when this file is passed to the python command on the command line: 
'python movie_tweets_collector.py'

In that method an array of directories is defined:
```
    files = [
        "data_sets/recent/",
        "data_sets/good/",
        "data_sets/bad/"
    ]
```

This is the structure that the directory in which you run this file should have. 
Within each of these directories (bad, recent, good) a JSON formatted file movies.json must be available. 
This file is where the list of movies you want to collect tweets about are listed as follows: 
```
{
    "sources": [
        "http://www.imdb.com/chart/bottom",
        "http://www.rottentomatoes.com/m/run_for_your_wife_2013/",
        "http://www.imdb.com/title/tt1333125/"
    ],
    "movies": [
        {
            "score": "2.5",
            "movie": "Blubberella"
        },
        {
            "score": "2.5",
            "movie": "Baby Geniuses"
        },
        ...
    ]
}
```
The "sources" key points to an array of URLs where our data for movies and their scores was taken from.
The "movies" key points to an array of objects, each with two keys: "score" pointing to the score out of 10 
and "movie" pointing to the title of the movie as found in the sources.

When the main method begins it loads the movies.json file from each directory in turn and iterates over them.
Before it begins it attempts to open a complete file containing, per line, a movie title that we already 
collected data for. This is so that we don't waste our API requests and go over our limit if errors occur 
(network, bad requests, timeout, etc.) Some of these errors are caught and we can continue, but some cannot be so 
we saved the ones completed so we wouldn't repeat requests. While iterating over the list of movies, we check if 
we have already processed the movie previously and if so we skip it. 
If we haven't processed it, we send a request for the movie to the Twitter search API (not the stream API). 
The search terms are generated in generate_search_terms and contain likely permutations and twitter-like ways of 
structuring the movie title in a tweet. Exact phrases and ORed phrases are included in the query and ultimately 
all the terms are ORed in the request. 
Before making the request, we must authenticate our API requests. This data is line by line in "auth.txt". Please
place your valid authentication data there before running the script.
The Cursor API allows us to specify at most 1000 tweets per movie and once that limit is reached we write all the data 
into tweets/[move_title].json formatted as
```
[
    {
        "tweet_text": "finally watched boyhood and im speechless wow"
    }, 
    {
        "tweet_text": "Have now seen 5 of the Best Pic nominees. 
                       Selma, Whiplash, Boyhood, Birdman, Imitation Game. To me, Whiplash CLEARLY the best."
    }
   
    },
    ...
]
```
The movie title is then written to the complete file. 
Any errors as a result of the Twitter API are logged in an error_log file. 

The JSON file of movies may contain UTF-8 characters and so may the complete.json file. Be aware of that fact. We
only dealt with a very limited number of movie titles with UTF-8 characters in them so this is not well tested.

The API will sleep if the rate limit is exceeded.


