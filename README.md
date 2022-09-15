# Rotten Tomatoes Python API


## How to use:
~~~python
from rotten_tomatoes import RottenTomatoesClient

# initialize RottenTomatoes client
client = RottenTomatoesClient()

# search movies or tv shows
from rotten_tomatoes import RottenTomatoesSearch
results = client.search('There Will Be Blood 2007', RottenTomatoesSearch.MOVIE)


# get exact movie
movie = client.get_movie('There Will Be Blood', 2007)

# response:
"""
    { 
        'title': 'There Will Be Blood', 
        'year': 2007, 
        'tomatometer_score': 91, 
        'tomatometter_reviews': 244, 
        'audience_score': 86, 
        'audience_count': 250000, 
        'genres': ['Drama'], 
        'rating': 'R', 
        'synopsis': 'Silver miner Daniel Plainview (...) he deviates into moral bankruptcy.'
    }
"""

# get exact tvshow

tvshow = client.get_tvshow('Game Of Thrones', 2011, 2019)

# response
"""
{
    'start_year': 2011, 
    'end_year': 2019, 
    'tomatometer_score': 89, 
    'tomatometter_reviews': None, 
    'audience_score': 85, 
    'audience_count': None, 
    'title': 'Game of Thrones', 
    'genres': ['Drama'], 
    'rating': None, 
    'synopsis': 'George R.R. Martin\'s (...) and Spain.'}
"""
~~~