from webscraping_contexts import *
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

    class IMDB_Film: # Partially unit-tested
        def title_and_year( film_id): # tested
            with IMDbContext.Film(film_id) as film:
                return film.title_and_year()

        def main_page( film_id):
            with IMDbContext.Film(film_id) as film:
                dd = {}
                dd.update( film.title_and_year() )
                dd.update( film.small_credits() )
                dd.update( film.details() )
                dd.update( {'genres' : film.genres() }) # tested
                return dd

        def taglines( film_id): #tested
            with IMDbContext.FilmTaglines(film_id) as film:
                return film.taglines()

        def two_taglines_at_random(film_id):
            with IMDbContext.FilmTaglines(film_id) as film:
                NUM_TAGLINES = 2
                taglines = list(film.taglines())
                random.shuffle( taglines)
                if len( taglines) < NUM_TAGLINES:
                    return taglines
                else:
                    return taglines[:NUM_TAGLINES]

        def production_companies( film_id): #tested
            with IMDbContext.FilmCompanyCredits( film_id) as film:
                return film.production_cos()

        def poster_urls( film_id):
            with IMDbContext.FilmPosters( film_id) as soup:
                base_url = f'https://www.imdb.com'
                viewer_urls = [base_url + rel for rel in IMDbContext.FilmImages.poster_relative_locations( soup)]
                return_vals = []
                for viewer_url in viewer_urls:
                    with SoupContext.Base(viewer_url) as soup:
                        return_vals.append([img['src'] for img in soup.find_all('img') if 'peek' not in img['class']][0])
                return return_vals

        def recommendations( film_id):
            with IMDbContext.Recommendations( film_id) as film:
                return film.all_recommendations()

    class IMDB_Person:  #  fully unit-tested
        def full_name( person_id):
            '''Accepts an IMDB person_id; returns the person's name.'''
            with IMDbContext.Person( person_id) as person:
                return person.full_name()

        def acting_filmography( person_id):
            '''Accepts an IMDB person_id; returns a set consisting of their acting filmography.  Voice-over work, uncredited roles, etc. are not included.'''
            with IMDbContext.Person( person_id) as person:
                return person.acting_filmography()

    class IMDB_Search:  #  fully unit-tested
        def by_person_name( person_name):
            '''Accepts a person's name, searches IMDB for it, and returns the top result.'''
            with IMDbContext.Search( person_name) as search:
                return search.first_person()

        def by_title_and_year( search_title, search_year):
            '''Searches IMDB for search_title, and selects the film released closest to search_year.  If search_year is None, returns the top result.'''
            with IMDbContext.Search( search_title) as search:
                all_search_results = search.films()
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
