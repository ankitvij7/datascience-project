Table A and Table B were obtained by crawling:
* IMDB (Link: http://www.imdb.com)
* Rotten Tomatoes (Link: http://www.rottentomatoes.com)

We collected > 3000 tuples from each site across a variety of movie genres.  We collected **3006** movies from rottenTomatoes and **N** from imdb.  The source of the data is not found in the data / schema but in the file name.  The Tuples are of the form:

####Attributes:
Url,Title,Score,Rating,Genre,Directed By,Written By,Box Office,Release Date,Runtime,Studio

####Meaning of the attributes is as below:
Url - The movie URL
Title - The title of the movie
Score - The score given to the movie out of 10
Rating - The rating assigned to the movie. Examples: PG-13, R, etc
Genre - The genre the movie falls under. Examples: Action, Comedy, etc
Directed By - The list of directors separated by a semicolon(;)
Written By - The list of writers separated by a semicolon(;)
Box Office - The amount of money made at the box office 
Release Date - The date of release of the movie
Runtime - The duration of the movie
Studio - The list of studios that products the move separated by a semicolon(;)

