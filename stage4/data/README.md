# Files Listing

* A.csv - Cleaned version of ImdbMovieDatabase.csv
* B.csv - Cleaned version of RottenTomatoesMovieDatabase.csv
* PredictedMatchedTuples.csv - Matched set Movies from A and B, using Best matcher from stage #2
* E.csv - Merged sets A and B
* G.csv - Labeled data for training our classifier.
* README.md - this file.

# Data Details
Table A & B were obtained by crawling and cleaning:
* IMDB (Link: http://www.imdb.com)
* Rotten Tomatoes (Link: http://www.rottentomatoes.com)

We collected > 3000 tuples from each site across a variety of movie genres.  We collected **3005** movies from rottenTomatoes and **3250** from imdb.  The source of the data is not found in the data / schema but in the file name.  The Tuples are of the form:

## Attributes:
ID,Title,Score,Rating,Genre,Directed By,Written By,Box Office,Release Date,Runtime,Studio

## Meaning of the attributes is as below:
1. ID - Unique IDentification of each tuple
1. Title - The title of the movie
1. Score - The score given to the movie out of 10
1. Rating - The rating assigned to the movie. Examples: PG-13, R, etc
1. Genre - A single Genre of the movie
1. Directed By - The primary director
1. Written By - The primary writer
1. Box Office - The amount of money made at the box office 
1. Release Date - The date of release of the movie
1. Runtime - The duration of the movie
1. Studio - The primary studio that produced the movie

