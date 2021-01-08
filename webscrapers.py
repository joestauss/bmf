from locators import SoupLocator
from webscraping_context_managers import *
import urllib.request
import re
import random

class Webscraper:
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

    class IMDB_Film:
        def title_and_year( film_id):
            with SoupContext.Film(film_id) as soup:
                return SoupLocator.IMDB.MainPage.title_and_year( soup)

        def main_page( film_id):
            with SoupContext.Film(film_id) as soup:
                dd = {}
                dd.update( SoupLocator.IMDB.MainPage.title_and_year( soup) )
                dd.update( SoupLocator.IMDB.MainPage.small_credits( soup) )
                dd.update( SoupLocator.IMDB.MainPage.details(soup) )
                dd.update( {'genres' : SoupLocator.IMDB.MainPage.genres(soup) })
                return dd

        def taglines( film_id):
            with SoupContext.Taglines(film_id) as soup:
                return SoupLocator.IMDB.taglines( soup)

        def two_taglines_at_random(film_id):
            with SoupContext.Taglines(film_id) as soup:
                NUM_TAGLINES = 2
                taglines = list(SoupLocator.IMDB.taglines( soup))
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
                viewer_urls = [base_url + rel for rel in SoupLocator.IMDB.Images.poster_relative_locations( soup)]
                return_vals = []
                for viewer_url in viewer_urls:
                    with SoupContext.Base(viewer_url) as soup:
                        return_vals.append([img['src'] for img in soup.find_all('img') if 'peek' not in img['class']][0])
                return return_vals

    class IMDB_Person:
        def full_name( person_id):
            '''Accepts an IMDB person_id; returns the person's name.'''
            with SoupContext.Person( person_id) as soup:
                return SoupLocator.IMDB.Person.full_name( soup)

        def acting_filmography( person_id):
            '''Accepts an IMDB person_id; returns a set consisting of their acting filmography.  Voice-over work, uncredited roles, etc. are not included.'''
            with SoupContext.Person( person_id) as soup:
                return SoupLocator.IMDB.Person.acting_filmography( soup)

    class IMDB_Search:
        def by_person_name( person_name):
            '''Accepts a person's name, searches IMDB for it, and returns the top result.'''
            with SoupContext.Search( person_name) as soup:
                return SoupLocator.IMDB.Search.person( soup)

        def by_title_and_year( search_title, search_year):
            '''Searches IMDB for search_title, and selects the film released closest to search_year.  If search_year is None, returns the top result.'''
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
            '''Look up name from IMDB person_id.  Convenience function that calls Webscraper.IMDB_Person.full_name.'''
            return Webscraper.IMDB_Person.full_name( person_id)

        def for_title_and_year( film_id):
            '''Look up (title, year) from IMDB film_id.  Convenience function that calls Webscraper.IMDB_Film.title_and_year.'''
            dd = Webscraper.IMDB_Film.title_and_year( film_id)
            return dd['title'], dd['year']
