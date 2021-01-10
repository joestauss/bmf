from utility_methods import SoupUtil
from bs4 import BeautifulSoup
import random
import re
from selenium.webdriver.common.by import By
from parsers import FilmParser

class SeleniumLocator:
    class Twitter:
        USERNAME_BOX = (By.NAME, "session[username_or_email]")
        PASSWORD_BOX = (By.NAME, "session[password]")
        LOGIN_BUTTON = (By.XPATH, "/html/body/div/div/div/div/main/div/div/div/div[1]/div[1]/div/form/div/div[3]/div")
        POST_TEXT_BOX = (By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div")

    class IMDB:
        RECS_LIST = (By.ID, "titleRecs")

class SoupLocator:
    class IMDB:
        class Person:
            def full_name( soup):
                return soup.find('title').text.split('-')[0].strip()

            def acting_filmography( soup):
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
                full_acting_credits = soup.find(class_='filmo-category-section').find_all(class_='filmo-row')
                return filmography_filter( full_acting_credits)

        class MainPage:
            def title_and_year( soup):
                title_div = soup.find('div', class_='title_wrapper')
                if title_div is None:
                    return None, None
                _, title, year = FilmParser.identify( title_div.h1.text.strip())
                return {'title': title, "year": year}

            def small_credits( soup):
                credits_div = soup.find_all('div', class_='credit_summary_item')
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

            def details( soup):
                details_div = soup.find('div', id='titleDetails')
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

        def taglines( soup):
                taglines = set()
                tagline_divs = soup.find_all('div', class_='soda')
                for tagline_div in tagline_divs:
                    tagline_text = tagline_div.text.strip()
                    if re.search("Be the first to contribute!", tagline_text):
                        break
                    taglines.add(tagline_text)
                return taglines

        class CompanyCredits:
            def production_cos( soup):
                production_cos = set()
                credits = soup.find(id='company_credits_content')
                prod_co_list = credits.find_all(class_='simpleList')[0]
                for prod_co in prod_co_list.find_all('li'):
                    prod_co_text = prod_co.a.text.strip()
                    production_cos.add(prod_co_text)
                return production_cos

        class Search:
            def films( soup):
                r = []
                result_categories = soup.find_all('div', class_='findSection')
                for category in result_categories:
                    if category.find('h3').text == 'Titles':
                        film_results = category.find_all('td', class_='result_text')
                        for result in film_results:
                            _, title, year = FilmParser.identify( result.text.strip().split(' aka ')[0])
                            film_id = result.find('a')['href'].split("/")[2]
                            r.append( (film_id, title, year))
                return r

            def person( soup):
                r = None
                result_categories = soup.find_all('div', class_='findSection')
                for category in result_categories:
                    if category.find('h3').text == 'Names':
                        name_results = category.find_all('td', class_='result_text')
                        r = StringLocator.person_id( name_results[0].find('a')['href'])
                return r

        class Images:
            def poster_relative_locations( soup):
                image_thumbnails = soup.find( 'div', id='media_index_thumbnail_grid')
                return { a['href'] for a in image_thumbnails.find_all('a') if not re.search('registration/signin',a['href'])}

class StringLocator:
    def dollar_amount( s):
        dollar_amounts = re.findall(r'\$[0-9,]+', s)
        for d in dollar_amounts:
            return int(d[1:].replace(',', ''))
        return None

    def minute_amount( s):
        minute_amounts = re.findall(r'[0-9]+ min', s)
        for m in minute_amounts:
            return int(m[:-4])
        return None

    def person_id( s):
        if re.search("nm\d+", s):
            return re.findall("nm\d+", s)[0]
        return None
