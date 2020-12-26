from utility_methods import SoupUtil, StringUtil
from bs4 import BeautifulSoup
import random
import re

class IMDB_Scraper():
    def scrape_main_page( imdb_id):
        scalar_attributes = ['title', 'year', 'budget', 'box_office', 'runtime']
        list_attributes   = ['actors', 'directors', 'writers', 'genres']
        dd = {}
        for s in scalar_attributes:
            dd[s] = None
        for l in list_attributes:
            dd[l] = set()

        try:
            url = f'https://www.imdb.com/title/{imdb_id}'
            soup = SoupUtil.soup_from_url( url)
        except:
            return dd

        title_div = soup.find('div', class_='title_wrapper')
        title_and_year = title_div.h1.text
        try:
            dd['year'] = int(title_and_year[-6:-2])
            dd['title'] = title_and_year[:-8]
        except:
            dd['year'] = None
            dd['title'] = title_and_year

        credits_div = soup.find_all('div', class_='credit_summary_item')
        try:
            temp_directors = credits_div[0].text.split('|')[0].split('\n')[2].split(',')
            for director in temp_directors:
                dd['directors'].add(director.split('(')[0].strip())
        except:
            pass

        try:
            temp_writers = credits_div[1].text.split('|')[0].split('\n')[2].split(',')
            for writer in temp_writers:
                dd['writers'].add(writer.split('(')[0].strip())
        except:
            pass

        try:
            temp_actors = credits_div[2].text.split('|')[0].split('\n')[2].split(',')
            for actor in temp_actors:
                dd['actors'].add(actor.split('(')[0].strip())
        except:
            pass

        details_div = soup.find('div', id='titleDetails')
        try:
            budget_div  = SoupUtil.search_in_soup( details_div, 'div', 'Budget')
            dd['budget'] = StringUtil.dollar_amount(budget_div.text)
        except:
            dd['budget'] = None

        try:
            boxOffice_div  = SoupUtil.search_in_soup( details_div, 'div', 'Cumulative Worldwide Gross')
            dd['box_office'] = StringUtil.dollar_amount(boxOffice_div.text)
        except:
            dd['box_office'] = None

        try:
            runtime_div = SoupUtil.search_in_soup( details_div, 'div', 'Runtime')
            dd['runtime'] = StringUtil.minute_amount( runtime_div.text)
        except:
            dd['runtime'] = None

        try:
            storyline_div = soup.find('div', id='titleStoryLine')
            genres_div  = SoupUtil. search_in_soup( storyline_div, 'div', 'Genre')

            genre_links = genres_div.find_all('a')
            genre_list = []
            for l in genre_links:
                genre_list.append( l.text.strip())
            dd['genres'] = set( genre_list)
        except:
            dd['genres'] = set()
        return dd

    def taglines(imdb_id, NUM_TAGLINES = 2):
        taglines = set()
        try:
            url = f'https://www.imdb.com/title/{imdb_id}/taglines'
            soup = SoupUtil.soup_from_url( url)

            tagline_divs = soup.find_all('div', class_='soda')
            random.shuffle(tagline_divs)
            for tagline_div in tagline_divs:
                tagline_text = tagline_div.text.strip()
                if len( taglines) == NUM_TAGLINES or re.search("Be the first to contribute!", tagline_text):
                    break
                taglines.add(tagline_text)
        finally:
            return taglines

    def production_companies( imdb_id):
        production_cos = set()
        try:
            url = f'https://www.imdb.com/title/{imdb_id}/companycredits'
            soup = SoupUtil.soup_from_url( url)

            credits = soup.find(id='company_credits_content')
            prod_co_list = credits.find_all(class_='simpleList')[0]
            for prod_co in prod_co_list.find_all('li'):
                prod_co_text = prod_co.a.text.strip()
                production_cos.add(prod_co_text)
        finally:
            return production_cos
