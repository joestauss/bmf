from utility_methods import *
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumLocator():
    class IMDB():
        def recommendations( imdb_id):
            URL = f"https://www.imdb.com/title/{imdb_id}/"
            driver = webdriver.Chrome()
            driver.get( URL)
            recs = []
            try:
                recs_div = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "titleRecs"))
                )
                recs_temp = recs_div.find_elements(By.CLASS_NAME, 'rec_item')
                for rec in recs_temp:
                    rec_str = rec.get_attribute("data-tconst")
                    if rec_str != imdb_id:
                        recs.append(rec_str)
            finally:
                driver.quit()
                return recs

class SoupLocator():
    class IMDB():
        class Search():
            def films( soup):
                r = [] # this is a list because order numbers.
                result_categories = soup.find_all('div', class_='findSection')
                for category in result_categories:
                    if category.find('h3').text == 'Titles':
                        film_results = category.find_all('td', class_='result_text')
                        for result in film_results:
                            _, title, year = StringUtil.film_identity( result.text.strip().split(' aka ')[0])
                            imdb_id = result.find('a')['href'].split("/")[2]
                            r.append( (imdb_id, title, year))
                return r

        class Person():
            def acting_filmography( soup):
                actor_filmography = soup.find(class_='filmo-category-section')
                full_acting_credits = actor_filmography.find_all(class_='filmo-row')
                return SoupUtil.filmography_filter( full_acting_credits)

        class MainPage():
            def title_and_year( soup):
                title_div = soup.find('div', class_='title_wrapper')
                if title_div is None:
                    return None, None
                _, title, year = StringUtil.film_identity( title_div.h1.text.strip())
                return title, year

            def small_credits( soup):
                credits_div = soup.find_all('div', class_='credit_summary_item')
                directors = set()
                try:
                    temp_directors = credits_div[0].text.split('|')[0].split('\n')[2].split(',')
                    for director in temp_directors:
                        directors.add(director.split('(')[0].strip())
                except:
                    pass

                writers = set()
                try:
                    temp_writers = credits_div[1].text.split('|')[0].split('\n')[2].split(',')
                    for writer in temp_writers:
                        writers.add(writer.split('(')[0].strip())
                except:
                    pass

                actors = set()
                try:
                    temp_actors = credits_div[2].text.split('|')[0].split('\n')[2].split(',')
                    for actor in temp_actors:
                        dd['actors'].add(actor.split('(')[0].strip())
                except:
                    pass
                return directors, writers, actors

            def details( soup):
                details_div = soup.find('div', id='titleDetails')
                try:
                    budget_div = SoupUtil.search_in_soup( details_div, 'div', 'Budget')
                    budget = StringUtil.dollar_amount(budget_div.text)
                except:
                    budget = None

                try:
                    boxOffice_div  = SoupUtil.search_in_soup( details_div, 'div', 'Cumulative Worldwide Gross')
                    box_office = StringUtil.dollar_amount(boxOffice_div.text)
                except:
                    box_office = None

                try:
                    runtime_div = SoupUtil.search_in_soup( details_div, 'div', 'Runtime')
                    runtime = StringUtil.minute_amount( runtime_div.text)
                except:
                    runtime = None

                return budget, box_office, runtime

            def genres( soup):
                genres = set()
                try:
                    storyline_div = soup.find('div', id='titleStoryLine')
                    genres_div  = SoupUtil. search_in_soup( storyline_div, 'div', 'Genre')

                    genre_links = genres_div.find_all('a')
                    for l in genre_links:
                        genres.add( l.text.strip())
                finally:
                    return genres

        class CompanyCredits():
            def production_cos( soup):
                production_cos = set()
                credits = soup.find(id='company_credits_content')
                prod_co_list = credits.find_all(class_='simpleList')[0]
                for prod_co in prod_co_list.find_all('li'):
                    prod_co_text = prod_co.a.text.strip()
                    production_cos.add(prod_co_text)
                return production_cos

        class Taglines():
            def get_two_at_random( soup):
                NUM_TAGLINES = 2
                taglines = set()
                tagline_divs = soup.find_all('div', class_='soda')
                random.shuffle(tagline_divs)
                for tagline_div in tagline_divs:
                    tagline_text = tagline_div.text.strip()
                    if len( taglines) == NUM_TAGLINES or re.search("Be the first to contribute!", tagline_text):
                        break
                    taglines.add(tagline_text)
                return taglines
