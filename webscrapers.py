from utility_methods import SoupUtil
from locators import SoupLocator
import re

class Webscraper():
    class IMDB():
        class Film():
            def title_and_year( imdb_id):
                url  = f'https://www.imdb.com/title/{imdb_id}'
                soup = SoupUtil.soup_from_url( url)
                return SoupLocator.IMDB.MainPage.title_and_year( soup)

            def main_page( imdb_id):
                url = f'https://www.imdb.com/title/{imdb_id}'
                soup = SoupUtil.soup_from_url( url)
                ttl_yr = SoupLocator.IMDB.MainPage.title_and_year( soup)
                sm_cst = SoupLocator.IMDB.MainPage.small_credits( soup)
                detail = SoupLocator.IMDB.MainPage.details(soup)
                genres = SoupLocator.IMDB.MainPage.genres(soup)
                return ttl_yr, sm_cst, detail, genres

            def taglines(imdb_id, NUM_TAGLINES = 2):
                url = f'https://www.imdb.com/title/{imdb_id}/taglines'
                soup = SoupUtil.soup_from_url( url)
                return SoupLocator.IMDB.Taglines.get_two_at_random( soup)

            def production_companies( imdb_id):
                url = f'https://www.imdb.com/title/{imdb_id}/companycredits'
                soup = SoupUtil.soup_from_url( url)
                return SoupLocator.IMDB.CompanyCredits.production_cos( soup)

        class Actor():
            def acting_filmography( imdb_id):
                if not re.match("nm\d+", imdb_id):
                    return []
                url = f'https://www.imdb.com/name/{imdb_id}/'
                soup = SoupUtil.soup_from_url( url)
                return SoupLocator.IMDB.Person.acting_filmography( soup)

        class Search():
            #   I've tried a few different names for the container class, and haven't been happy with any of them.
            #   "Identify" somehow feels vague in this context, and "Search" felt natural when calling these methods.
            #
            def for_title_and_year( imdb_id):
                url  = f'https://www.imdb.com/title/{imdb_id}'
                soup = SoupUtil.soup_from_url( url)
                return SoupLocator.IMDB.MainPage.title_and_year( soup)

            def by_title_and_year( search_title, search_year):
                #   Eventually, add search by title and year.
                #
                url = f"https://www.imdb.com/find?q={search_title}"
                soup = SoupUtil.soup_from_url( url)
                candidates = SoupLocator.IMDB.Search.films( soup)

                smallest_difference = 2000
                return_id   = None
                return_year = None
                for imdb_id, title, year in candidates:
                    if search_year is None:
                        return imdb_id, year
                    if title == search_title:
                        if abs(year - search_year) < smallest_difference:
                            return_id, return_year = imdb_id, year
                            smallest_difference = abs(year - search_year)
                return return_id, return_year

            def by_person_name( person_name):
                url = f"https://www.imdb.com/find?q={person_name}"
                soup = SoupUtil.soup_from_url( url)
                return SoupLocator.IMDB.Search.person( soup)

            def for_person_name( person_id):
                url  = f'https://www.imdb.com/name/{person_id}'
                soup = SoupUtil.soup_from_url( url)
                return SoupLocator.IMDB.Person.full_name( soup)
