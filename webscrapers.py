from utility_methods import *
from locators import SoupLocator
from webscraping_context_managers import *
import re

class Webscraper():
    class IMDB():
        class Film():
            def title_and_year( imdb_id):
                with SoupContext.Film(imdb_id) as soup:
                    return SoupLocator.IMDB.MainPage.title_and_year( soup)

            def main_page( imdb_id):
                with SoupContext.Film(imdb_id) as soup:
                    ttl_yr = SoupLocator.IMDB.MainPage.title_and_year( soup)
                    sm_cst = SoupLocator.IMDB.MainPage.small_credits( soup)
                    detail = SoupLocator.IMDB.MainPage.details(soup)
                    genres = SoupLocator.IMDB.MainPage.genres(soup)
                    return ttl_yr, sm_cst, detail, genres

            def taglines( imdb_id):
                with SoupContext.Taglines(imdb_id) as soup:
                    return SoupLocator.IMDB.taglines( soup)

            def two_taglines_at_random(imdb_id):
                with SoupContext.Taglines(imdb_id) as soup:
                    NUM_TAGLINES = 2
                    taglines = SoupLocator.IMDB.taglines( soup)
                    random.shuffle( taglines)
                    if len( taglines) < NUM_TAGLINES:
                        return taglines
                    else:
                        return taglines[:NUM_TAGLINES]

            def production_companies( imdb_id):
                with SoupContext.CompanyCredits( imdb_id) as soup:
                    return SoupLocator.IMDB.CompanyCredits.production_cos( soup)

        class Actor():
            def full_name( actor_id):
                with SoupContext.Actor( actor_id) as soup:
                    return SoupLocator.IMDB.Person.full_name( soup)

            def acting_filmography( actor_id):
                with SoupContext.Actor( actor_id) as soup:
                    return SoupLocator.IMDB.Person.acting_filmography( soup)

        class Search():
            #   I've tried a few different names for the container class, and haven't been happy with any of them.
            #   "Identify" somehow feels vague in this context, and "Search" felt natural when calling these methods.
            #
            #   The "Search for" methods just call other methods in this module, but I'm experimenting with front-ends.
            #
            def for_title_and_year( imdb_id):
                return Webscraper.IMDB.Film.title_and_year( imdb_id)

            def by_title_and_year( search_title, search_year):
                with SoupContext.Search( search_title) as soup:
                    all_search_results = SoupLocator.IMDB.Search.films( soup)
                    if not all_search_results:
                        return None
                    candidates = [(id, year) for (id, title, year) in all_search_results if title == search_title]
                    if search_year is None:
                        return candidates[0]
                    else:
                        year_offsets = {(id, year): abs(year - search_year) for (id, year) in candidates }
                        return min( year_offsets, key=year_offsets.get)

            def for_person_name( person_id):
                return Webscraper.IMDB.Actor.full_name( person_id)

            def by_person_name( person_name):
                with SoupContext.Search( person_name) as soup:
                    return SoupLocator.IMDB.Search.person( soup)
