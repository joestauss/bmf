import requests
import re
import random
from bs4 import BeautifulSoup

class IMDB_Data():
    def __init__(self, imdb_id):
        self.imdb_id = imdb_id
        self.scrape_all()

    def __str__(self):
        description =     [ f"IMDB ID:\t{self.imdb_id}"]
        description.append( f"Title:\t\t{self.title}")
        description.append( f"Year:\t\t{self.year}")
        description.append( f"Genres:\t\t{self.genres}")
        return "\n".join( description)

    def as_dict(self):
        dd = {
            'movie_id' : self.imdb_id,
            'movie_title' : self.title,
            'movie_year' : self.year,
            'movie_budget' : self.budget,
            'movie_boxoffice' : self.box_office,
            'movie_runtime': self.runtime
        }
        return dd

    def scrape_all(self):
        self.scrape_movie_data()
        self.scrape_taglines()
        self.scrape_production_cos()

    def scrape_taglines(self):
        self.taglines = set()
        NUM_TAGLINES = 2
        url = f'https://www.imdb.com/title/{self.imdb_id}/taglines'
        r       =   requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        tagline_divs = soup.find_all('div', class_='soda')

        try:
            selected_taglines = random.sample(tagline_divs, NUM_TAGLINES)
        except:
            selected_taglines = tagline_divs
        for tagline in selected_taglines:
            try:
                self.taglines.add(tagline.text.strip())
            except:
                pass

    def scrape_production_cos(self):
        self.production_cos = set()
        url = f'https://www.imdb.com/title/{self.imdb_id}/companycredits'
        r       =   requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        production_lst = soup.find_all('ul', class_='simpleList')

        for tag in production_lst:
            try:
                self.production_cos.add(tag.a.text)
            except:
                pass

    def scrape_movie_data(self):
        base_url =  f"https://www.imdb.com/title/{self.imdb_id}/"
        r       =   requests.get(base_url)
        soup    =   BeautifulSoup(r.text, 'html.parser')

        title_div = soup.find('div', class_='title_wrapper')
        title_and_year = title_div.h1.text
        try:
            self.year = int(title_and_year[-6:-2])
            self.title = title_and_year[:-8]
        except:
            self.year = None
            self.title = title_and_year

        credits_div = soup.find_all('div', class_='credit_summary_item')

        self.directors = set()
        try:
            temp_directors = credits_div[0].text.split('|')[0].split('\n')[2].split(',')
            for director in temp_directors:
                self.directors.add(director.split('(')[0].strip())
        except:
            pass

        self.writers = set()
        try:
            temp_writers = credits_div[1].text.split('|')[0].split('\n')[2].split(',')
            for writer in temp_writers:
                self.writers.add(writer.split('(')[0].strip())
        except:
            pass

        self.actors = set()
        try:
            temp_actors = credits_div[2].text.split('|')[0].split('\n')[2].split(',')
            for actor in temp_actors:
                self.actors.add(actor.split('(')[0].strip())
        except:
            pass

        details_div = soup.find('div', id='titleDetails')
        try:
            budget_div  = my_webscraping.search_in_soup( details_div, 'div', 'Budget')
            self.budget = my_utility.find_dollar_amount(budget_div.text)
        except:
            self.budget = None

        try:
            boxOffice_div  = my_webscraping.search_in_soup( details_div, 'div', 'Cumulative Worldwide Gross')
            self.box_office = my_utility.find_dollar_amount(boxOffice_div.text)
        except:
            self.box_office = None

        try:
            runtime_div = my_webscraping.search_in_soup( details_div, 'div', 'Runtime')
            self.runtime = my_utility.find_minute_amount( runtime_div.text)
        except:
            self.runtime = None

        try:
            storyline_div = soup.find('div', id='titleStoryLine')
            genres_div  = search_in_soup( storyline_div, 'div', 'Genre')

            genre_links = genres_div.find_all('a')
            genre_list = []
            for l in genre_links:
                genre_list.append( l.text.strip())
            self.genres = set( genre_list)
        except:
            self.genres = set()


# search_in_soup
# Looks inside of soup for a BeautifulSoup object with a base tag of tag_type
# containing search_text, and returns the first success.
#
def search_in_soup(soup, tag_type, search_text):
    candidates = soup.find_all(tag_type)

    for c in candidates:
        tag_text = c.text
        if re.search(search_text, tag_text):
            return c
    return None
