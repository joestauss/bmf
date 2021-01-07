from utility_methods import *
from locators import SoupLocator
from webscraping_context_managers import *
import urllib.request
import re

class Webscraper():
    def image( url, target_file_location):
        ''' Downloads an image.

        Parameters
        ----------
        url: string
          URL to the image to be downloaded.

        target_file_location: os.path
            The loation where the file will be written to.  It overwrites whatever is at that location.

        Returns
        -------
        Nothing.
        '''
        with SoupContext.Base(url) as soup:
            urllib.request.urlretrieve(url, target_file_location)

    class IMDB():
        class Film():
            def title_and_year( film_id):
                with SoupContext.Film(film_id) as soup:
                    return SoupLocator.IMDB.MainPage.title_and_year( soup)

            def main_page( film_id):
                with SoupContext.Film(film_id) as soup:
                    ttl_yr = SoupLocator.IMDB.MainPage.title_and_year( soup)
                    sm_cst = SoupLocator.IMDB.MainPage.small_credits( soup)
                    detail = SoupLocator.IMDB.MainPage.details(soup)
                    genres = SoupLocator.IMDB.MainPage.genres(soup)
                    return ttl_yr, sm_cst, detail, genres

            def taglines( film_id):
                with SoupContext.Taglines(film_id) as soup:
                    return SoupLocator.IMDB.taglines( soup)

            def two_taglines_at_random(film_id):
                with SoupContext.Taglines(film_id) as soup:
                    NUM_TAGLINES = 2
                    taglines = SoupLocator.IMDB.taglines( soup)
                    random.shuffle( taglines)
                    if len( taglines) < NUM_TAGLINES:
                        return taglines
                    else:
                        return taglines[:NUM_TAGLINES]

            def production_companies( film_id):
                with SoupContext.CompanyCredits( film_id) as soup:
                    return SoupLocator.IMDB.CompanyCredits.production_cos( soup)

            def poster_urls( film_id):
                with SoupContext.Posters( film_id) as soup:
                    base_url = f'https://www.imdb.com'
                    return [base_url + rel for rel in SoupLocator.IMDB.Images.poster_relative_locations( soup)]

        class Person:
            def full_name( person_id):
                with SoupContext.Person( person_id) as soup:
                    return SoupLocator.IMDB.Person.full_name( soup)

            def acting_filmography( person_id):
                with SoupContext.Person( person_id) as soup:
                    return SoupLocator.IMDB.Person.acting_filmography( soup)

        class Search():
            #   I've tried a few different names for the container class, and haven't been happy with any of them.
            #   "Identify" somehow feels vague in this context, and "Search" felt natural when calling these methods.
            #
            #   The "Search for" methods just call other methods in this module, but I'm experimenting with front-ends.
            #
            def for_title_and_year( film_id):
                return Webscraper.IMDB.Film.title_and_year( film_id)

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
                return Webscraper.IMDB.Person.full_name( person_id)

            def by_person_name( person_name):
                with SoupContext.Search( person_name) as soup:
                    return SoupLocator.IMDB.Search.person( soup)
