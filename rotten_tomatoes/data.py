import urllib
from typing import Union, List, TYPE_CHECKING
from .utils import int_or_none
if TYPE_CHECKING:
    from .scraper import Scraper


class RottenTomatesObject(dict):
    title:str
    tomatometer_score:int
    tomatometter_reviews:int
    audience_score:int
    audience_count:int
    genres:List[str]
    rating:str
    synopsis:str
    def __init__(self, 
    tomatometer_score:int = None, 
    audience_score:int = None, 
    tomatometter_reviews:int = None, 
    audience_count:int = None, 
    title = None,
    genres = None,
    rating = None,
    synopsis = None,
    **kwargs,
    ) -> None:
        self.tomatometer_score = int_or_none(tomatometer_score)
        self.tomatometter_reviews = int_or_none(tomatometter_reviews)
        self.audience_score = int_or_none(audience_score) 
        self.audience_count = int_or_none(audience_count)
        self.title = title
        self.genres = genres
        self.rating = rating
        self.synopsis = synopsis
    
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()


class Movie(RottenTomatesObject):
    year:Union[int, None]
    def __init__(self, *args, **kwargs) -> None:
        self.year = int_or_none(kwargs.get('year', None))
        super().__init__(*args, **kwargs)

class TVShow(RottenTomatesObject):
    start_year:Union[int, None]
    end_year:Union[int, None]
    def __init__(self, *args, **kwargs) -> None:
        self.start_year = int_or_none(kwargs.get('start_year', None))
        self.end_year = int_or_none(kwargs.get('end_year', None))
        super().__init__(*args, **kwargs)


class SearchResultItem:
    def __init__(self, title:str, url:str, scraper:'Scraper') -> None:
        self.title = title
        self.url = url
        self.scraper = scraper

    def get_details(self) -> Union[Movie, TVShow]:
        path_splited = urllib.parse.urlparse(self.url).path.split('/')
        if len(path_splited) >= 2:
            flag = path_splited[1]
            # flags: 'm' or 'tv'
            if flag == 'm':
                return self.scraper.scrape_movie_details(self.url)
            if flag == 'tv':
                return self.scraper.scrape_tvshow_details(self.url)
