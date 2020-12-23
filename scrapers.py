from utility_methods import SoupUtil
from bs4 import BeautifulSoup
import random
import re

class IMDB_Scraper():
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
