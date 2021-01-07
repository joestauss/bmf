import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webscrapers import *

class SeleniumContext:
    class BasicChromeDriver():
        def __init__( self, url):
            self.url = url

        def __enter__(self):
            self.driver = webdriver.Chrome()
            self.driver.get(self.url)
            return self.driver

        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.driver.quit()

class SoupContext():
    class Base():
        def __init__( self, url):
            self.url = url

        def __enter__(self):
            response       = requests.get( self.url)
            self.base_soup = BeautifulSoup( response.text, 'html.parser')
            return self.base_soup

        def __exit__(self, exc_type, exc_value, exc_traceback):
            pass

    class Search( Base):
        def __init__(self, search_term):
            self.url = f"https://www.imdb.com/find?q={search_term}"

    class Person( Base):
        def __init__(self, person_id):
            self.person_id = person_id
            if not re.match("nm\d+", self.person_id):
                raise ValueError(f"person context called invalid person ID: {self.person_id}")
            self.url = f'https://www.imdb.com/name/{person_id}/'

    class Film( Base):
        def __init__(self, film_id):
            self.film_id = film_id
            if not re.match("tt\d+", self.film_id):
                raise ValueError(f"Film context called with invalid film ID {self.film_id}")
            self.url = f'https://www.imdb.com/title/{film_id}'

    class Taglines( Film):
        def __init__(self, film_id):
            super().__init__(film_id)
            self.url = self.url + "/taglines"

    class CompanyCredits( Film):
        def __init__(self, film_id):
            super().__init__(film_id)
            self.url = self.url + "/companycredits"

    class Posters( Film):
        def __init__(self, film_id):
            super().__init__(film_id)
            self.url = self.url + "/mediaindex?refine=poster"
