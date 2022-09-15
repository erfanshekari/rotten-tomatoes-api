import requests
from typing import Callable, List
from bs4 import BeautifulSoup
from unidecode import unidecode
from .data import Movie, TVShow, SearchResultItem
from .utils import export_digits

class Scraper:
    def get_html(url):
        return requests.get(url).text

    def parse(html):
        return BeautifulSoup(html, 'html.parser')
    
    def error_handler(self, func:Callable):
        try:
            return func()
        except Exception as exc:
            raise exc

    def search(self, url:str, topic:str) -> List[SearchResultItem]:
        endpoint = url
        results = []
        def search():
            parsed_page = Scraper.parse(
                Scraper.get_html(endpoint)
                )
            results_group = parsed_page.find_all('search-page-result')
            for result in results_group:
                title = None
                title_ = result.find('h2')
                if title_ and title_.text:
                    title = title_.text.lower()
                if title == topic:
                    items = result.find('ul').find_all('search-page-media-row')
                    for item in items:
                        links = item.find_all('a')
                        if len(links) >= 2:
                            title = links[1].text
                            url =  links[1].get('href')
                            if title and url:
                                results.append(SearchResultItem(title = unidecode(title.strip()), url = url, scraper = self))
                    break
        self.error_handler(search)
        return results

    def scrape_movie_details(self, url:str) -> Movie:
        def scrape_movie_details():
            parsed_page = Scraper.parse(Scraper.get_html(url))
            score_board = parsed_page.find('score-board')
            if score_board:
                title = score_board.find('h1').text
                year, genres, duration = None, None, None
                tomatometter_reviews = None
                audience_count = None
                audience_score = score_board.get('audiencescore')
                tomatometer_score = score_board.get('tomatometerscore')
                rating = score_board.get('rating')
                info = score_board.find('p')
                if info:
                    year, _, duration = info.text.split(',')
                for element in score_board.find_all('a'):
                    if element.get('slot') == 'critics-count':
                        tomatometter_reviews = export_digits(element.text)
                    if element.get('slot') == 'audience-count':
                        audience_count = export_digits(element.text)

                info = parsed_page.find('section', {'data-qa': 'movie-info-section'})

                synopsis = info.find('div', { 'data-qa' : 'movie-info-synopsis' })
                if synopsis:
                    synopsis = synopsis.text.strip()
                
                genres = info.find('div', { 
                    'data-qa' : 'movie-info-item-value',
                    'class' : 'genre',
                    })
                if genres:
                    genres = genres.text.strip().split(',')

                return Movie(
                    title = title,
                    year = year, 
                    genres = genres,
                    duration = duration, 
                    tomatometer_score = tomatometer_score, 
                    tomatometter_reviews = tomatometter_reviews, 
                    audience_count = audience_count, 
                    audience_score = audience_score, 
                    rating = rating,
                    synopsis = synopsis)
        return self.error_handler(scrape_movie_details)

    def scrape_tvshow_details(self, url:str) -> TVShow:
        def scrape_tvshow_details():
            parsed_page = Scraper.parse(Scraper.get_html(url))
            if parsed_page:
                title = None
                tomatometer_score = None
                audience_score = None
                for element in parsed_page.find_all('h1'):
                    if element.get('data-type') == 'title':
                        title = (lambda E: E[0] if E else None)(element.text.strip().split('\n'))
                        years = element.find('span')
                        if years:
                            start_year, end_year = (
                                years.text
                                .strip()
                                .replace('(', '')
                                .replace(')', '')
                                .replace(' ', '')
                                .split('-')
                                )
                            start_year = export_digits(start_year)
                            end_year = export_digits(end_year)
                        break
                for element in parsed_page.find('section', {'class': 'mop-ratings-wrap__info'}).find_all('span'):
                    if element.get('data-qa') == 'tomatometer':
                        tomatometer_score = export_digits(element.text.strip().replace('%', ''))
                    if element.get('data-qa') == 'audience-score':
                        audience_score = export_digits(element.text.strip().replace('%', ''))
                genre = (parsed_page
                .find('section', {'id': 'detail_panel'})
                .find('table')
                .find('td', {'data-qa': 'series-details-genre'})
                .text)
                synopsis = parsed_page.find('div', { 'id': 'movieSynopsis' })
                if synopsis:
                    synopsis = synopsis.text.strip()
                return TVShow(
                    title = title, 
                    tomatometer_score = tomatometer_score, 
                    audience_score = audience_score, 
                    start_year = start_year, 
                    end_year = end_year, 
                    genres = [genre],
                    synopsis = synopsis
                )
        return self.error_handler(scrape_tvshow_details)