from FilmRecord import *
from browser_automation import *
import threading
from webscrapers import *

class BaseFilmCollection():
    RECORD_TYPE = BaseFilmRecord
    def __init__(self, input_list, VERBOSE=False):
        self.movies = set()
        for i, input_item in enumerate(input_list, 1):
            if VERBOSE:
                print( f"Adding record {i} of {len(input_list)}:\t{input_item}")
            self.add_record( input_item)

    def __str__(self):
        r = [ StringUtil.section_header("Film Collection")]
        sorted_movies = sorted( self.movies, key=lambda m:m.year if m.year else 0)
        for item in sorted_movies:
            r.append( str(item))
        return "\n".join(r)

    def add_record( self, item):
        imdb_id, title, year = StringUtil.film_identity( item)
        if not imdb_id:
            imdb_id, _ = IMDB_Scraper.search_by_title_and_year( title, year)
        self.movies.add( self.RECORD_TYPE( imdb_id))

    def identify_all( self):
        threads = {}
        for movie in self.movies:
            threads[movie] = threading.Thread( target=movie.identify)
            threads[movie].start()
        for movie in self.movies:
            threads[movie].join()

    def scrape_all( self):
        threads = {}
        counter = 0
        for movie in self.movies:
            counter = counter + 1
            print(f"Creating thread {counter}.")
            threads[movie] = threading.Thread( target=movie.scrape_data)
            threads[movie].start()
        for movie in self.movies:
            print(f"Waiting for {counter} threads..")
            threads[movie].join()
            counter = counter - 1


class TaglineFilmCollection( BaseFilmCollection):
    RECORD_TYPE = TaglineFilmRecord

class DetailedFilmCollection( BaseFilmCollection):
    RECORD_TYPE = DetailedFilmRecord

class ExpandableFilmCollection( BaseFilmCollection):
    def __init__(self, input_list):
        super().__init__(input_list)
        self.identify_all()

    def full_recommendation_expansion(self):
        imdb_ids = { movie.imdb_id for movie in self.movies }
        recs = DataExtraction.Recommendations.all(imdb_ids)
        for rec in recs:
            self.add_record( rec)

        num_old = len( imdb_ids )
        num_new = len( recs - imdb_ids )
        num_total = len( recs)
        print(f"From {num_old} films, there were {num_total} recommendations, of which {num_new} are new.")
        self.identify_all()
