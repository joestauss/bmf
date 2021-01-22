import re
import requests
import pyparsing as pp
from bs4 import BeautifulSoup
from parsers import FilmParser
from chopping_block import SoupUtil

class IMDbContext:
    class Base():
        NAME_ID  = pp.Combine( pp.Literal("nm") + pp.Word( pp.nums))
        TITLE_ID = pp.Combine( pp.Literal("tt") + pp.Word( pp.nums))

        def __init__( self, url):
            self.url = url

        def __enter__(self):
            response       = requests.get( self.url)
            if response.status_code == requests.codes.ok:
                self.soup = BeautifulSoup( response.text, 'html.parser')
                return self
            else:
                response.raise_for_status() # raises an error

        def __exit__(self, exc_type, exc_value, exc_traceback):
            pass

    class Film( Base):
        def __init__(self, film_id):
            self.film_id = film_id
            if not re.match("tt\d+", self.film_id):
                raise ValueError(f"Film context called with invalid film ID {self.film_id}")
            self.url = f'https://www.imdb.com/title/{film_id}'

        def title_and_year( self):
            title_div = self.soup.find('div', class_='title_wrapper')
            if title_div is None:
                return None, None
            _, title, year = FilmParser.identify( title_div.h1.text.strip())
            return {'title': title, "year": year}

        def small_credits( self):
            credits_div = self.soup.find_all('div', class_='credit_summary_item')
            roles = ['directors', 'writers', 'actors']
            cast = {role : set()  for role in roles }
            for i, role in enumerate( roles):
                try:
                    temp = credits_div[i].text.split('|')[0].split('\n')[2].split(',')
                    for person in temp:
                        cast[role].add(person.split('(')[0].strip())
                except:
                    pass
            return cast

        def details( self):
            details_div = self.soup.find('div', id='titleDetails')
            details = [('budget', 'Budget'), ('box_office', 'Cumulative Worldwide Gross'), ('runtime', 'Runtime')]
            dd = {key: None for (key, _) in details}
            for key, search_term in details:
                try:
                    data_div = SoupUtil.search_in_soup( details_div, 'div', search_term)
                    if key in ['budget', 'box_office']:
                        dd[ key] = StringLocator.dollar_amount(data_div.text)
                    if key in ['runtime']:
                        dd[ key] = StringLocator.minute_amount(data_div.text)
                except:
                    pass
            return dd

        def genres( self):
            genres = set()
            try:
                storyline_div = self.soup.find('div', id='titleStoryLine')
                genres_div  = SoupUtil. search_in_soup( storyline_div, 'div', 'Genre')

                genre_links = genres_div.find_all('a')
                for l in genre_links:
                    genres.add( l.text.strip())
            finally:
                return genres

    class FilmCompanyCredits( Film):
        def __init__(self, film_id):
            super().__init__(film_id)
            self.url = self.url + "/companycredits"

        def production_cos( self):
            production_cos = set()
            credits = self.soup.find(id='company_credits_content')
            prod_co_list = credits.find_all(class_='simpleList')[0]
            for prod_co in prod_co_list.find_all('li'):
                prod_co_text = prod_co.a.text.strip()
                production_cos.add(prod_co_text)
            return production_cos

    class FilmImages( Film):
        def poster_relative_locations( self):
            image_thumbnails = self.soup.find( 'div', id='media_index_thumbnail_grid')
            return { a['href'] for a in image_thumbnails.find_all('a') if not re.search('registration/signin',a['href'])}

    class FilmPosters( Film):
        def __init__(self, film_id):
            super().__init__(film_id)
            self.url = self.url + "/mediaindex?refine=poster"

    class FilmTaglines( Film):
        def __init__(self, film_id):
            super().__init__(film_id)
            self.url = self.url + "/taglines"

        def taglines( self):
                taglines = set()
                tagline_divs = self.soup.find_all('div', class_='soda')
                for tagline_div in tagline_divs:
                    tagline_text = tagline_div.text.strip()
                    if re.search("Be the first to contribute!", tagline_text):
                        break
                    taglines.add(tagline_text)
                return taglines

    class Person( Base):
        def __init__(self, person_id):
            self.person_id = person_id
            if not re.match("nm\d+", self.person_id):
                raise ValueError(f"person context called invalid person ID: {self.person_id}")
            self.url = f'https://www.imdb.com/name/{person_id}/'

        def full_name( self):
            return self.soup.find('title').text.split('-')[0].strip()

        def acting_filmography( self):
            def filmography_filter( full_filmography):
                r_vals = []
                illegal_patterns = [
                    "(Video Game)", "(TV Series)", "uncredited", "(TV Movie)",
                    "(Video short)", "(Video)", "(TV Special)", "(Short)", "(scenes deleted)",
                    "(TV Mini-Series)", "(Documentary)", "(Concert Feature)", "(voice)"
                ]
                for item in full_filmography:
                    REGULAR_FILM = True
                    for illegal_pattern in illegal_patterns:
                        if re.search(illegal_pattern, item.text) :
                            REGULAR_FILM = False
                    if REGULAR_FILM:
                        r_vals.append( FilmParser.identify( item.find('a')["href"])[0])
                return r_vals
            full_acting_credits = self.soup.find(class_='filmo-category-section').find_all(class_='filmo-row')
            return filmography_filter( full_acting_credits)

    class Search( Base):
        def __init__(self, search_term):
            self.url = f"https://www.imdb.com/find?q={search_term}"

        def films( self):
            r = []
            result_categories = self.soup.find_all('div', class_='findSection')
            for category in result_categories:
                if category.find('h3').text == 'Titles':
                    film_results = category.find_all('td', class_='result_text')
                    for result in film_results:
                        try:
                            _, title, year = FilmParser.identify( result.text.strip().split(' aka ')[0])
                            film_id = result.find('a')['href'].split("/")[2]
                            r.append( (film_id, title, year))
                        except:
                            pass
            return r

        def first_person( self):
            r = None
            result_categories = self.soup.find_all('div', class_='findSection')
            for category in result_categories:
                if category.find('h3').text == 'Names':
                    name_results = category.find_all('td', class_='result_text')
                    r = self.NAME_ID.searchString( name_results[0].find('a')['href'])[0][0]
            return r
