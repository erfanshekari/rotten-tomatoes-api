from typing import List, TYPE_CHECKING
from enum import Enum
from unidecode import unidecode
from .scraper import Scraper
from .utils import get_close_matches_indexes
if TYPE_CHECKING:
    from .data import Movie, TVShow, SearchResultItem
    

URL = 'https://www.rottentomatoes.com/'

class RottenTomatoesSearch(Enum):
    MOVIE = 'movies'
    TVSHOW = 'tv shows'


class RottenTomatoesClient:
    def __init__(self) -> None:
        self.scraper = Scraper()

    def search(self, key:str, filter:RottenTomatoesSearch) -> List['SearchResultItem']:
        return self.scraper.search(
            url = f'{URL}search?search={key}',
            topic = filter.value,
        )

    def find_matches(self, key:str, items: List['SearchResultItem']):
        titles = [item.title for item in items]
        matches = []
        for index in get_close_matches_indexes(key, titles):
            matches.append(items[index])
        return matches
                
    def get_movie(self, title:str, year:int) -> 'Movie':
        cleaned_title = unidecode(title).strip()
        results = self.search(f'{cleaned_title} {year}', RottenTomatoesSearch.MOVIE)
        if results:
            matches = self.find_matches(title, results)
            for match in matches:
                movie = match.get_details()
                if movie.title and movie.year:
                    if movie.year == year:
                        return movie

   
    def get_tvshow(self, title:str, start_year:int, end_year:int = None) -> 'TVShow':
        cleaned_title = unidecode(title).strip()
        results = self.search(f'{cleaned_title} {start_year}', RottenTomatoesSearch.TVSHOW)
        if results:
            matches = self.find_matches(title, results)
            for match in matches:
                tvshow = match.get_details()
                if tvshow and tvshow.start_year == start_year:
                    if end_year:
                        if not tvshow.end_year: return
                        if end_year == tvshow.end_year: return tvshow
                        else: return
                    return tvshow
